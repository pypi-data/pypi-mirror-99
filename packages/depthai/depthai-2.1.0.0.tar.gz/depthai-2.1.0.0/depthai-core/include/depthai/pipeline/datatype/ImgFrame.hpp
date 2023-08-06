#pragma once

#include <chrono>
#include <unordered_map>
#include <vector>

#include "depthai-shared/datatype/RawImgFrame.hpp"
#include "depthai/pipeline/datatype/Buffer.hpp"

// optional
#ifdef DEPTHAI_OPENCV_SUPPORT
    #include <opencv2/opencv.hpp>
#endif

namespace dai {

/**
 * ImgFrame message. Carries image data and metadata.
 */
class ImgFrame : public Buffer {
    std::shared_ptr<RawBuffer> serialize() const override;
    RawImgFrame& img;

   public:
    // Raw* mirror
    using Type = RawImgFrame::Type;
    using Specs = RawImgFrame::Specs;

    /**
     * Construct ImgFrame message.
     * Timestamp is set to now
     */
    ImgFrame();
    explicit ImgFrame(std::shared_ptr<RawImgFrame> ptr);
    virtual ~ImgFrame() = default;

    // getters
    /**
     * Retrievies image timestamp related to steady_clock / time.monotonic
     */
    std::chrono::time_point<std::chrono::steady_clock, std::chrono::steady_clock::duration> getTimestamp() const;

    /**
     * Retrievies instance number
     */
    unsigned int getInstanceNum() const;

    /**
     * Retrievies image category
     */
    unsigned int getCategory() const;

    /**
     * Retrievies image sequence number
     */
    unsigned int getSequenceNum() const;

    /**
     * Retrievies image width in pixels
     */
    unsigned int getWidth() const;

    /**
     * Retrievies image height in pixels
     */
    unsigned int getHeight() const;

    /**
     * Retrieves image type
     */
    Type getType() const;

    // setters
    /**
     * Specifies current timestamp, related to steady_clock / time.monotonic
     */
    void setTimestamp(std::chrono::time_point<std::chrono::steady_clock, std::chrono::steady_clock::duration> timestamp);

    /**
     * Instance number relates to the origin of the frame (which camera)
     *
     * @param instance Instance number
     */
    void setInstanceNum(unsigned int instance);

    /**
     * @param category Image category
     */
    void setCategory(unsigned int category);

    /**
     * Specifies sequence number
     *
     * @param seq Sequence number
     */
    void setSequenceNum(unsigned int seq);

    /**
     * Specifies frame width
     *
     * @param width frame width
     */
    void setWidth(unsigned int width);

    /**
     * Specifies frame height
     *
     * @param width frame height
     */
    void setHeight(unsigned int);

    /**
     * Specifies frame type, RGB, BGR, ...
     *
     * @param type Type of image
     */
    void setType(Type type);

// Optional - OpenCV support
#ifdef DEPTHAI_OPENCV_SUPPORT
    /**
     * @note This API only available if OpenCV support enabled
     *
     * Copies cv::Mat data to ImgFrame buffer
     *
     * @param frame Input cv::Mat frame from which to copy the data
     */
    void setFrame(cv::Mat frame);

    /**
     * @note This API only available if OpenCV support enabled
     *
     * Retrieves data as cv::Mat with specified width, height and type
     *
     * @param copy If false only a reference to data is made, otherwise a copy
     * @returns cv::Mat with corresponding to ImgFrame parameters
     */
    cv::Mat getFrame(bool copy = false);

    /**
     * @note This API only available if OpenCV support enabled
     *
     * Retrieves cv::Mat suitable for use in common opencv functions.
     * ImgFrame is converted to color BGR interleaved or grayscale depending on type.
     *
     * A copy is always made
     *
     * @returns cv::Mat for use in opencv functions
     */
    cv::Mat getCvFrame();
#endif
};

}  // namespace dai
