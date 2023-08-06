#include "depthai/device/Device.hpp"

// std
#include <iostream>

// shared
#include "depthai-bootloader-shared/Bootloader.hpp"
#include "depthai-bootloader-shared/XLinkConstants.hpp"
#include "depthai-shared/datatype/RawImgFrame.hpp"
#include "depthai-shared/log/LogConstants.hpp"
#include "depthai-shared/log/LogLevel.hpp"
#include "depthai-shared/log/LogMessage.hpp"
#include "depthai-shared/pipeline/Assets.hpp"
#include "depthai-shared/xlink/XLinkConstants.hpp"

// project
#include "DeviceLogger.hpp"
#include "depthai/pipeline/node/XLinkIn.hpp"
#include "depthai/pipeline/node/XLinkOut.hpp"
#include "pipeline/Pipeline.hpp"
#include "utility/BootloaderHelper.hpp"
#include "utility/Initialization.hpp"
#include "utility/PimplImpl.hpp"
#include "utility/Resources.hpp"

// libraries
#include "spdlog/sinks/stdout_color_sinks.h"
#include "spdlog/spdlog.h"

namespace dai {

// local static function
static LogLevel spdlogLevelToLogLevel(spdlog::level::level_enum level, LogLevel defaultValue = LogLevel::OFF) {
    switch(level) {
        case spdlog::level::trace:
            return LogLevel::TRACE;
        case spdlog::level::debug:
            return LogLevel::DEBUG;
        case spdlog::level::info:
            return LogLevel::INFO;
        case spdlog::level::warn:
            return LogLevel::WARN;
        case spdlog::level::err:
            return LogLevel::ERR;
        case spdlog::level::critical:
            return LogLevel::CRITICAL;
        case spdlog::level::off:
            return LogLevel::OFF;
        // Default
        case spdlog::level::n_levels:
        default:
            return defaultValue;
            break;
    }
    // Default
    return defaultValue;
}
static spdlog::level::level_enum logLevelToSpdlogLevel(LogLevel level, spdlog::level::level_enum defaultValue = spdlog::level::off) {
    switch(level) {
        case LogLevel::TRACE:
            return spdlog::level::trace;
        case LogLevel::DEBUG:
            return spdlog::level::debug;
        case LogLevel::INFO:
            return spdlog::level::info;
        case LogLevel::WARN:
            return spdlog::level::warn;
        case LogLevel::ERR:
            return spdlog::level::err;
        case LogLevel::CRITICAL:
            return spdlog::level::critical;
        case LogLevel::OFF:
            return spdlog::level::off;
    }
    // Default
    return defaultValue;
}

// Common explicit instantiation, to remove the need to define in header
template std::tuple<bool, DeviceInfo> Device::getAnyAvailableDevice(std::chrono::nanoseconds);
template std::tuple<bool, DeviceInfo> Device::getAnyAvailableDevice(std::chrono::microseconds);
template std::tuple<bool, DeviceInfo> Device::getAnyAvailableDevice(std::chrono::milliseconds);
template std::tuple<bool, DeviceInfo> Device::getAnyAvailableDevice(std::chrono::seconds);
constexpr std::chrono::seconds Device::DEFAULT_SEARCH_TIME;
constexpr std::size_t Device::EVENT_QUEUE_MAXIMUM_SIZE;
constexpr float Device::DEFAULT_SYSTEM_INFORMATION_LOGGING_RATE_HZ;

template <typename Rep, typename Period>
std::tuple<bool, DeviceInfo> Device::getAnyAvailableDevice(std::chrono::duration<Rep, Period> timeout) {
    using namespace std::chrono;
    constexpr auto POOL_SLEEP_TIME = milliseconds(100);

    // First looks for UNBOOTED, then BOOTLOADER, for 'timeout' time
    auto searchStartTime = steady_clock::now();
    bool found = false;
    DeviceInfo deviceInfo;
    do {
        for(auto searchState : {X_LINK_UNBOOTED, X_LINK_BOOTLOADER}) {
            std::tie(found, deviceInfo) = XLinkConnection::getFirstDevice(searchState);
            if(found) break;
        }
        if(found) break;

        // If 'timeout' < 'POOL_SLEEP_TIME', use 'timeout' as sleep time and then break
        if(timeout < POOL_SLEEP_TIME) {
            // sleep for 'timeout'
            std::this_thread::sleep_for(timeout);
            break;
        } else {
            std::this_thread::sleep_for(POOL_SLEEP_TIME);  // default pool rate
        }
    } while(steady_clock::now() - searchStartTime < timeout);

    // If none were found, try BOOTED
    if(!found) std::tie(found, deviceInfo) = XLinkConnection::getFirstDevice(X_LINK_BOOTED);

    return {found, deviceInfo};
}

// Default overload ('DEFAULT_SEARCH_TIME' timeout)
std::tuple<bool, DeviceInfo> Device::getAnyAvailableDevice() {
    return getAnyAvailableDevice(DEFAULT_SEARCH_TIME);
}

// static api

// First tries to find UNBOOTED device, then BOOTLOADER device
std::tuple<bool, DeviceInfo> Device::getFirstAvailableDevice() {
    bool found;
    DeviceInfo dev;
    std::tie(found, dev) = XLinkConnection::getFirstDevice(X_LINK_UNBOOTED);
    if(!found) {
        std::tie(found, dev) = XLinkConnection::getFirstDevice(X_LINK_BOOTLOADER);
    }
    return {found, dev};
}

// Returns all devices which aren't already booted
std::vector<DeviceInfo> Device::getAllAvailableDevices() {
    std::vector<DeviceInfo> availableDevices;
    auto connectedDevices = XLinkConnection::getAllConnectedDevices();
    for(const auto& d : connectedDevices) {
        if(d.state != X_LINK_BOOTED) availableDevices.push_back(d);
    }
    return availableDevices;
}

// First tries to find UNBOOTED device with mxId, then BOOTLOADER device with mxId
std::tuple<bool, DeviceInfo> Device::getDeviceByMxId(std::string mxId) {
    std::vector<DeviceInfo> availableDevices;
    auto states = {X_LINK_UNBOOTED, X_LINK_BOOTLOADER};
    bool found;
    DeviceInfo dev;
    for(const auto& state : states) {
        std::tie(found, dev) = XLinkConnection::getDeviceByMxId(mxId, state);
        if(found) return {true, dev};
    }
    return {false, DeviceInfo()};
}

std::vector<std::uint8_t> Device::getEmbeddedDeviceBinary(bool usb2Mode, OpenVINO::Version version) {
    return Resources::getInstance().getDeviceFirmware(usb2Mode, version);
}

/*
std::vector<DeviceInfo> Device::getAllConnectedDevices(){
    return XLinkConnection::getAllConnectedDevices();
}


std::tuple<bool, DeviceInfo> Device::getFirstDevice(){
    return XLinkConnection::getFirstAvailableDevice();
}
*/

///////////////////////////////////////////////
// Impl section - use this to hide dependencies
///////////////////////////////////////////////
class Device::Impl {
   public:
    Impl() = default;

    // Default sink
    std::shared_ptr<spdlog::sinks::stdout_color_sink_mt> stdoutColorSink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
    // Device Logger
    DeviceLogger logger{"", stdoutColorSink};

    void setLogLevel(LogLevel level);
    LogLevel getLogLevel();
    void setPattern(const std::string& pattern);
};

void Device::Impl::setPattern(const std::string& pattern) {
    logger.set_pattern(pattern);
}

void Device::Impl::setLogLevel(LogLevel level) {
    // Converts LogLevel to spdlog and reconfigures logger level
    auto spdlogLevel = logLevelToSpdlogLevel(level, spdlog::level::warn);
    // Set level for all configured sinks
    logger.set_level(spdlogLevel);
}

LogLevel Device::Impl::getLogLevel() {
    // Converts spdlog to LogLevel
    return spdlogLevelToLogLevel(logger.level(), LogLevel::WARN);
}

///////////////////////////////////////////////
// END OF Impl section
///////////////////////////////////////////////

Device::Device(const Pipeline& pipeline, const DeviceInfo& devInfo, bool usb2Mode) : deviceInfo(devInfo) {
    init(pipeline, true, usb2Mode, "");
}

Device::Device(const Pipeline& pipeline, const DeviceInfo& devInfo, const char* pathToCmd) : deviceInfo(devInfo) {
    init(pipeline, false, false, std::string(pathToCmd));
}

Device::Device(const Pipeline& pipeline, const DeviceInfo& devInfo, const std::string& pathToCmd) : deviceInfo(devInfo) {
    init(pipeline, false, false, pathToCmd);
}

Device::Device(const Pipeline& pipeline) {
    // Searches for any available device for 'default' timeout

    bool found = false;
    std::tie(found, deviceInfo) = getAnyAvailableDevice();

    // If no device found, throw
    if(!found) throw std::runtime_error("No available devices");
    init(pipeline, true, false, "");
}

Device::Device(const Pipeline& pipeline, const char* pathToCmd) {
    // Searches for any available device for 'default' timeout

    bool found = false;
    std::tie(found, deviceInfo) = getAnyAvailableDevice();

    // If no device found, throw
    if(!found) throw std::runtime_error("No available devices");
    init(pipeline, false, false, std::string(pathToCmd));
}

Device::Device(const Pipeline& pipeline, const std::string& pathToCmd) {
    // Searches for any available device for 'default' timeout
    bool found = false;
    std::tie(found, deviceInfo) = getAnyAvailableDevice();

    // If no device found, throw
    if(!found) throw std::runtime_error("No available devices");
    init(pipeline, false, false, pathToCmd);
}

Device::Device(const Pipeline& pipeline, bool usb2Mode) {
    // Searches for any available device for 'default' timeout
    bool found = false;
    std::tie(found, deviceInfo) = getAnyAvailableDevice();

    // If no device found, throw
    if(!found) throw std::runtime_error("No available devices");
    init(pipeline, true, usb2Mode, "");
}

void Device::close() {
    // Only allow to close once
    if(closed.exchange(true)) return;

    using namespace std::chrono;
    auto t1 = steady_clock::now();
    spdlog::debug("Device about to be closed...");

    // Remove callbacks to this from queues
    for(const auto& kv : callbackIdMap) {
        outputQueueMap[kv.first]->removeCallback(kv.second);
    }
    // Clear map
    callbackIdMap.clear();

    // Close connection first (so queues unblock)
    connection->close();
    connection = nullptr;

    // Clear queues
    outputQueueMap.clear();
    inputQueueMap.clear();

    // Stop watchdog
    watchdogRunning = false;
    timesyncRunning = false;
    loggingRunning = false;

    // Stop watchdog first (this resets and waits for link to fall down)
    if(watchdogThread.joinable()) watchdogThread.join();
    // Then stop timesync
    if(timesyncThread.joinable()) timesyncThread.join();
    // And at the end stop logging thread
    if(loggingThread.joinable()) loggingThread.join();

    // Close rpcStream
    rpcStream = nullptr;

    spdlog::debug("Device closed, {}", duration_cast<milliseconds>(steady_clock::now() - t1).count());
}

bool Device::isClosed() const {
    return closed || !watchdogRunning;
}

void Device::checkClosed() const {
    if(isClosed()) throw std::invalid_argument("Device already closed or disconnected");
}

Device::~Device() {
    close();
}

void Device::init(const Pipeline& pipeline, bool embeddedMvcmd, bool usb2Mode, const std::string& pathToMvcmd) {
    // Initalize depthai library if not already
    initialize();

    // Mark the OpenVINO version and serialize the pipeline
    pipeline.serialize(schema, assets, assetStorage, version);

    spdlog::debug("Device - pipeline serialized, OpenVINO version: {}", OpenVINO::getVersionName(version));

    // Set logging pattern of device (device id + shared pattern)
    pimpl->setPattern(fmt::format("[{}] {}", deviceInfo.getMxId(), LOG_DEFAULT_PATTERN));

    // Get embedded mvcmd
    std::vector<std::uint8_t> embeddedFw = Resources::getInstance().getDeviceFirmware(usb2Mode, version);

    // Init device (if bootloader, handle correctly - issue USB boot command)
    if(deviceInfo.state == X_LINK_UNBOOTED) {
        // Unbooted device found, boot and connect with XLinkConnection constructor
        if(embeddedMvcmd) {
            connection = std::make_shared<XLinkConnection>(deviceInfo, embeddedFw);
        } else {
            connection = std::make_shared<XLinkConnection>(deviceInfo, pathToMvcmd);
        }

    } else if(deviceInfo.state == X_LINK_BOOTLOADER) {
        // Scope so bootloaderConnection is desctructed and XLink cleans its state
        {
            // Bootloader state, proceed by issuing a command to bootloader
            XLinkConnection bootloaderConnection(deviceInfo, X_LINK_BOOTLOADER);

            // Open stream
            XLinkStream stream(bootloaderConnection, bootloader::XLINK_CHANNEL_BOOTLOADER, bootloader::XLINK_STREAM_MAX_SIZE);
            streamId_t streamId = stream.getStreamId();

            // // Send request for bootloader version
            // if(!sendBootloaderRequest(streamId, bootloader::request::GetBootloaderVersion{})){
            //     throw std::runtime_error("Error trying to connect to device");
            // }
            // // Receive response
            // dai::bootloader::response::BootloaderVersion ver;
            // if(!receiveBootloaderResponse(streamId, ver)) throw std::runtime_error("Error trying to connect to device");

            // Send request to jump to USB bootloader
            // Boot into USB ROM BOOTLOADER NOW
            if(!sendBootloaderRequest(streamId, dai::bootloader::request::UsbRomBoot{})) {
                throw std::runtime_error("Error trying to connect to device");
            }

            // Dummy read, until link falls down and it returns an error code
            streamPacketDesc_t* pPacket;
            XLinkReadData(streamId, &pPacket);
        }

        // After that the state is UNBOOTED
        deviceInfo.state = X_LINK_UNBOOTED;

        // Boot and connect with XLinkConnection constructor
        if(embeddedMvcmd) {
            connection = std::make_shared<XLinkConnection>(deviceInfo, embeddedFw);
        } else {
            connection = std::make_shared<XLinkConnection>(deviceInfo, pathToMvcmd);
        }

    } else if(deviceInfo.state == X_LINK_BOOTED) {
        // Connect without booting
        if(embeddedMvcmd) {
            connection = std::make_shared<XLinkConnection>(deviceInfo, embeddedFw);
        } else {
            connection = std::make_shared<XLinkConnection>(deviceInfo, pathToMvcmd);
        }
    } else {
        throw std::runtime_error("Cannot find any device with given deviceInfo");
    }

    deviceInfo.state = X_LINK_BOOTED;

    // prepare rpc for both attached and host controlled mode
    rpcStream = std::unique_ptr<XLinkStream>(new XLinkStream(*connection, dai::XLINK_CHANNEL_MAIN_RPC, dai::XLINK_USB_BUFFER_MAX_SIZE));

    client = std::unique_ptr<nanorpc::core::client<nanorpc::packer::nlohmann_msgpack>>(
        new nanorpc::core::client<nanorpc::packer::nlohmann_msgpack>([this](nanorpc::core::type::buffer request) {
            std::unique_lock<std::mutex>(this->rpcMutex);

            // Log the request data
            if(spdlog::get_level() == spdlog::level::trace) {
                spdlog::trace("RPC: {}", nlohmann::json::from_msgpack(request).dump());
            }

            // Send request to device
            rpcStream->write(std::move(request));

            // Receive response back
            // Send to nanorpc to parse
            return rpcStream->read();
        }));

    // prepare watchdog thread, which will keep device alive
    watchdogThread = std::thread([this]() {
        std::shared_ptr<XLinkConnection> conn = this->connection;
        while(watchdogRunning) {
            try {
                client->call("watchdogKeepalive");
            } catch(const std::exception& ex) {
                break;
            }
            // Ping with a period half of that of the watchdog timeout
            std::this_thread::sleep_for(XLINK_WATCHDOG_TIMEOUT / 2);
        }

        // Watchdog ended. Useful for checking disconnects
        watchdogRunning = false;
    });

    // prepare timesync thread, which will keep device synchronized
    timesyncThread = std::thread([this]() {
        using namespace std::chrono;

        try {
            XLinkStream stream(*this->connection, XLINK_CHANNEL_TIMESYNC, 128);
            Timestamp timestamp = {};
            while(timesyncRunning) {
                // Block
                stream.read();

                // Timestamp
                auto d = std::chrono::steady_clock::now().time_since_epoch();
                timestamp.sec = duration_cast<seconds>(d).count();
                timestamp.nsec = duration_cast<nanoseconds>(d).count() % 1000000000;

                // Write timestamp back
                stream.write(&timestamp, sizeof(timestamp));
            }
        } catch(const std::exception& ex) {
            // ignore
            spdlog::debug("Timesync thread exception caught: {}", ex.what());
        }

        timesyncRunning = false;
    });

    // prepare logging thread, which will log device messages
    loggingThread = std::thread([this]() {
        using namespace std::chrono;
        std::vector<LogMessage> messages;
        try {
            XLinkStream stream(*this->connection, XLINK_CHANNEL_LOG, 128);
            while(loggingRunning) {
                // Block
                auto log = stream.read();

                // parse packet as msgpack
                try {
                    auto j = nlohmann::json::from_msgpack(log);
                    // create pipeline schema from retrieved data
                    nlohmann::from_json(j, messages);

                    spdlog::trace("Log vector decoded, size: {}", messages.size());

                    // log the messages in incremental order (0 -> size-1)
                    for(const auto& msg : messages) {
                        pimpl->logger.logMessage(msg);
                    }

                    // Log to callbacks
                    {
                        // lock mtx to callback map (shared)
                        std::unique_lock<std::mutex> l(logCallbackMapMtx);
                        for(const auto& msg : messages) {
                            for(const auto& kv : logCallbackMap) {
                                const auto& cb = kv.second;
                                // If available, callback with msg
                                if(cb) cb(msg);
                            }
                        }
                    }

                } catch(const nlohmann::json::exception& ex) {
                    spdlog::error("Exception while parsing or calling callbacks for log message from device: {}", ex.what());
                }
            }
        } catch(const std::exception& ex) {
            // ignore exception from logging
            spdlog::debug("Log thread exception caught: {}", ex.what());
        }

        loggingRunning = false;
    });

    // Below can throw - make sure to gracefully exit threads
    try {
        // Set logging level (if DEPTHAI_LEVEL lower than warning, then device is configured accordingly as well)
        if(spdlog::get_level() < spdlog::level::warn) {
            auto level = spdlogLevelToLogLevel(spdlog::get_level());
            setLogLevel(level);
            setLogOutputLevel(level);
        } else {
            setLogLevel(LogLevel::WARN);
            setLogOutputLevel(LogLevel::WARN);
        }

        // Sets system inforation logging rate. By default 1s
        setSystemInformationLoggingRate(DEFAULT_SYSTEM_INFORMATION_LOGGING_RATE_HZ);

        // Open queues upfront, let queues know about data sizes (input queues)
        // Go through Pipeline and check for 'XLinkIn' and 'XLinkOut' nodes
        // and create corresponding default queues for them
        for(const auto& kv : pipeline.getNodeMap()) {
            const auto& node = kv.second;
            const auto& xlinkIn = std::dynamic_pointer_cast<const node::XLinkIn>(node);
            if(xlinkIn == nullptr) {
                continue;
            }
            // Create DataInputQueue's
            inputQueueMap[xlinkIn->getStreamName()] = std::make_shared<DataInputQueue>(connection, xlinkIn->getStreamName());
            // set max data size, for more verbosity
            inputQueueMap[xlinkIn->getStreamName()]->setMaxDataSize(xlinkIn->getMaxDataSize());
        }
        for(const auto& kv : pipeline.getNodeMap()) {
            const auto& node = kv.second;
            const auto& xlinkOut = std::dynamic_pointer_cast<const node::XLinkOut>(node);
            if(xlinkOut == nullptr) {
                continue;
            }

            auto streamName = xlinkOut->getStreamName();
            // Create DataOutputQueue's
            outputQueueMap[streamName] = std::make_shared<DataOutputQueue>(connection, streamName);

            // Add callback for events
            callbackIdMap[streamName] = outputQueueMap[streamName]->addCallback([this](std::string queueName, std::shared_ptr<ADatatype>) {
                // Lock first
                std::unique_lock<std::mutex> lock(eventMtx);

                // Check if size is equal or greater than EVENT_QUEUE_MAXIMUM_SIZE
                if(eventQueue.size() >= EVENT_QUEUE_MAXIMUM_SIZE) {
                    auto numToRemove = eventQueue.size() - EVENT_QUEUE_MAXIMUM_SIZE + 1;
                    eventQueue.erase(eventQueue.begin(), eventQueue.begin() + numToRemove);
                }

                // Add to the end of event queue
                eventQueue.push_back(queueName);

                // notify the rest
                eventCv.notify_all();
            });
        }

    } catch(const std::exception& ex) {
        // close device (cleanup)
        close();
        // Rethrow original exception
        throw;
    }
}

std::shared_ptr<DataOutputQueue> Device::getOutputQueue(const std::string& name) {
    checkClosed();

    // Throw if queue not created
    // all queues for xlink streams are created upfront
    if(outputQueueMap.count(name) == 0) {
        throw std::runtime_error(fmt::format("Queue for stream name '{}' doesn't exist", name));
    }
    // Return pointer to this DataQueue
    return outputQueueMap.at(name);
}

std::shared_ptr<DataOutputQueue> Device::getOutputQueue(const std::string& name, unsigned int maxSize, bool blocking) {
    checkClosed();

    // Throw if queue not created
    // all queues for xlink streams are created upfront
    if(outputQueueMap.count(name) == 0) {
        throw std::runtime_error(fmt::format("Queue for stream name '{}' doesn't exist", name));
    }

    // Modify max size and blocking
    outputQueueMap.at(name)->setMaxSize(maxSize);
    outputQueueMap.at(name)->setBlocking(blocking);

    // Return pointer to this DataQueue
    return outputQueueMap.at(name);
}

std::vector<std::string> Device::getOutputQueueNames() const {
    checkClosed();

    std::vector<std::string> names;
    names.reserve(outputQueueMap.size());
    for(const auto& kv : outputQueueMap) {
        names.push_back(kv.first);
    }
    return names;
}

std::shared_ptr<DataInputQueue> Device::getInputQueue(const std::string& name) {
    checkClosed();

    // Throw if queue not created
    // all queues for xlink streams are created upfront
    if(inputQueueMap.count(name) == 0) {
        throw std::runtime_error(fmt::format("Queue for stream name '{}' doesn't exist", name));
    }
    // Return pointer to this DataQueue
    return inputQueueMap.at(name);
}

std::shared_ptr<DataInputQueue> Device::getInputQueue(const std::string& name, unsigned int maxSize, bool blocking) {
    checkClosed();

    // Throw if queue not created
    // all queues for xlink streams are created upfront
    if(inputQueueMap.count(name) == 0) {
        throw std::runtime_error(fmt::format("Queue for stream name '{}' doesn't exist", name));
    }

    // Modify max size and blocking
    inputQueueMap.at(name)->setMaxSize(maxSize);
    inputQueueMap.at(name)->setBlocking(blocking);

    // Return pointer to this DataQueue
    return inputQueueMap.at(name);
}

std::vector<std::string> Device::getInputQueueNames() const {
    checkClosed();

    std::vector<std::string> names;
    names.reserve(inputQueueMap.size());
    for(const auto& kv : inputQueueMap) {
        names.push_back(kv.first);
    }
    return names;
}

// void Device::setCallback(const std::string& name, std::function<std::shared_ptr<RawBuffer>(std::shared_ptr<RawBuffer>)> cb) {
//     // creates a CallbackHandler if not yet created
//     if(callbackMap.count(name) == 0) {
//         throw std::runtime_error(fmt::format("Queue for stream name '{}' doesn't exist", name));
//     } else {
//         // already exists, replace the callback
//         callbackMap.at(name).setCallback(cb);
//     }
// }

std::vector<std::string> Device::getQueueEvents(const std::vector<std::string>& queueNames, std::size_t maxNumEvents, std::chrono::microseconds timeout) {
    checkClosed();

    // First check if specified queues names are actually opened
    auto availableQueueNames = getOutputQueueNames();
    for(const auto& outputQueue : queueNames) {
        bool found = false;
        for(const auto& availableQueueName : availableQueueNames) {
            if(outputQueue == availableQueueName) {
                found = true;
                break;
            }
        }
        if(!found) throw std::runtime_error(fmt::format("Queue with name '{}' doesn't exist", outputQueue));
    }

    // Blocking part
    // lock eventMtx
    std::unique_lock<std::mutex> lock(eventMtx);

    // Create temporary string which predicate will fill when it finds the event
    std::vector<std::string> eventsFromQueue;
    // wait until predicate
    auto predicate = [this, &queueNames, &eventsFromQueue, &maxNumEvents]() {
        for(auto it = eventQueue.begin(); it != eventQueue.end();) {
            bool wasRemoved = false;
            for(const auto& name : queueNames) {
                if(name == *it) {
                    // found one of the events we have specified to wait for
                    eventsFromQueue.push_back(name);
                    // remove element from queue
                    it = eventQueue.erase(it);
                    wasRemoved = true;
                    // return and acknowledge the wait prematurelly, if reached maxnumevents
                    if(eventsFromQueue.size() >= maxNumEvents) {
                        return true;
                    }
                    // breaks as other queue names won't be same as this one
                    break;
                }
            }
            // If element wasn't removed, move iterator forward, else it was already moved by erase call
            if(!wasRemoved) ++it;
        }
        // After search, if no events were found, return false
        if(eventsFromQueue.empty()) return false;
        // Otherwise acknowledge the wait and exit
        return true;
    };

    if(timeout < std::chrono::microseconds(0)) {
        // if timeout < 0, infinite wait time (no timeout)
        eventCv.wait(lock, predicate);
    } else {
        // otherwise respect timeout
        eventCv.wait_for(lock, timeout, predicate);
    }

    // eventFromQueue should now contain the event name
    return eventsFromQueue;
}

std::vector<std::string> Device::getQueueEvents(const std::initializer_list<std::string>& queueNames,
                                                std::size_t maxNumEvents,
                                                std::chrono::microseconds timeout) {
    return getQueueEvents(std::vector<std::string>(queueNames), maxNumEvents, timeout);
}

std::vector<std::string> Device::getQueueEvents(std::string queueName, std::size_t maxNumEvents, std::chrono::microseconds timeout) {
    return getQueueEvents(std::vector<std::string>{queueName}, maxNumEvents, timeout);
}

std::vector<std::string> Device::getQueueEvents(std::size_t maxNumEvents, std::chrono::microseconds timeout) {
    return getQueueEvents(getOutputQueueNames(), maxNumEvents, timeout);
}

std::string Device::getQueueEvent(const std::vector<std::string>& queueNames, std::chrono::microseconds timeout) {
    auto events = getQueueEvents(queueNames, 1, timeout);
    if(events.empty()) return "";
    return events[0];
}
std::string Device::getQueueEvent(const std::initializer_list<std::string>& queueNames, std::chrono::microseconds timeout) {
    return getQueueEvent(std::vector<std::string>{queueNames}, timeout);
}

std::string Device::getQueueEvent(std::string queueName, std::chrono::microseconds timeout) {
    return getQueueEvent(std::vector<std::string>{queueName}, timeout);
}

std::string Device::getQueueEvent(std::chrono::microseconds timeout) {
    return getQueueEvent(getOutputQueueNames(), timeout);
}

// Convinience functions for querying current system information
MemoryInfo Device::getDdrMemoryUsage() {
    checkClosed();

    return client->call("getDdrUsage").as<MemoryInfo>();
}

MemoryInfo Device::getCmxMemoryUsage() {
    checkClosed();

    return client->call("getCmxUsage").as<MemoryInfo>();
}

MemoryInfo Device::getLeonCssHeapUsage() {
    checkClosed();

    return client->call("getLeonCssHeapUsage").as<MemoryInfo>();
}

MemoryInfo Device::getLeonMssHeapUsage() {
    checkClosed();

    return client->call("getLeonMssHeapUsage").as<MemoryInfo>();
}

ChipTemperature Device::getChipTemperature() {
    checkClosed();

    return client->call("getChipTemperature").as<ChipTemperature>();
}

CpuUsage Device::getLeonCssCpuUsage() {
    checkClosed();

    return client->call("getLeonCssCpuUsage").as<CpuUsage>();
}

CpuUsage Device::getLeonMssCpuUsage() {
    checkClosed();

    return client->call("getLeonMssCpuUsage").as<CpuUsage>();
}

bool Device::isPipelineRunning() {
    checkClosed();

    return client->call("isPipelineRunning").as<bool>();
}

void Device::setLogLevel(LogLevel level) {
    checkClosed();

    client->call("setLogLevel", level);
}

LogLevel Device::getLogLevel() {
    checkClosed();

    return client->call("getLogLevel").as<LogLevel>();
}

void Device::setLogOutputLevel(LogLevel level) {
    checkClosed();

    pimpl->setLogLevel(level);
}

LogLevel Device::getLogOutputLevel() {
    checkClosed();

    return pimpl->getLogLevel();
}

int Device::addLogCallback(std::function<void(LogMessage)> callback) {
    checkClosed();

    // Lock first
    std::unique_lock<std::mutex> l(logCallbackMapMtx);

    // Get unique id
    int id = uniqueCallbackId++;

    // assign callback
    logCallbackMap[id] = callback;

    // return id assigned to the callback
    return id;
}

bool Device::removeLogCallback(int callbackId) {
    checkClosed();

    // Lock first
    std::unique_lock<std::mutex> l(logCallbackMapMtx);

    // If callback with id 'callbackId' doesn't exists, return false
    if(logCallbackMap.count(callbackId) == 0) return false;

    // Otherwise erase and return true
    logCallbackMap.erase(callbackId);
    return true;
}

void Device::setSystemInformationLoggingRate(float rateHz) {
    checkClosed();

    client->call("setSystemInformationLoggingRate", rateHz);
}

float Device::getSystemInformationLoggingRate() {
    checkClosed();

    return client->call("getSystemInformationLoggingrate").as<float>();
}

bool Device::startPipeline() {
    checkClosed();

    // first check if pipeline is not already started
    if(isPipelineRunning()) return false;

    // if debug
    if(spdlog::get_level() == spdlog::level::debug) {
        nlohmann::json jSchema = schema;
        spdlog::debug("Schema dump: {}", jSchema.dump());
        nlohmann::json jAssets = assets;
        spdlog::debug("Asset map dump: {}", jAssets.dump());
    }

    // Load pipelineDesc, assets, and asset storage
    client->call("setPipelineSchema", schema);

    // Transfer storage != empty
    if(!assetStorage.empty()) {
        client->call("setAssets", assets);

        // allocate, returns a pointer to memory on device side
        auto memHandle = client->call("memAlloc", static_cast<std::uint32_t>(assetStorage.size())).as<uint32_t>();

        // Transfer the whole assetStorage in a separate thread
        const std::string streamAssetStorage = "__stream_asset_storage";
        std::thread t1([this, &streamAssetStorage]() {
            XLinkStream stream(*connection, streamAssetStorage, XLINK_USB_BUFFER_MAX_SIZE);
            int64_t offset = 0;
            do {
                int64_t toTransfer = std::min(static_cast<int64_t>(XLINK_USB_BUFFER_MAX_SIZE), static_cast<int64_t>(assetStorage.size() - offset));
                stream.write(&assetStorage[offset], toTransfer);
                offset += toTransfer;
            } while(offset < static_cast<int64_t>(assetStorage.size()));
        });

        // Open a channel to transfer AssetStorage
        client->call("readFromXLink", streamAssetStorage, memHandle, assetStorage.size());
        t1.join();

        // After asset storage is transfers, set the asset storage
        client->call("setAssetStorage", memHandle, assetStorage.size());
    }

    // print assets on device side for test
    client->call("printAssets");

    // Build and start the pipeline
    bool success = false;
    std::string errorMsg;
    std::tie(success, errorMsg) = client->call("buildPipeline").as<std::tuple<bool, std::string>>();
    if(success) {
        client->call("startPipeline");
    } else {
        throw std::runtime_error(errorMsg);
        return false;
    }

    return true;
}

}  // namespace dai
