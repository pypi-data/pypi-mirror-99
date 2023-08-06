#pragma once

#include "depthai/pipeline/Node.hpp"

// shared
#include "depthai-shared/properties/StereoDepthProperties.hpp"

namespace dai {
namespace node {

/**
 * @brief StereoDepth node. Compute stereo disparity and depth from left-right image pair.
 */
class StereoDepth : public Node {
    using Properties = dai::StereoDepthProperties;
    Properties properties;

    std::string getName() const override;
    std::vector<Output> getOutputs() override;
    std::vector<Input> getInputs() override;
    nlohmann::json getProperties() override;
    std::shared_ptr<Node> clone() override;

   public:
    StereoDepth(const std::shared_ptr<PipelineImpl>& par, int64_t nodeId);

    /**
     * Input for left ImgFrame of left-right pair
     *
     * Default queue is non-blocking with size 8
     */
    Input left{*this, "left", Input::Type::SReceiver, false, 8, {{DatatypeEnum::ImgFrame, true}}};

    /**
     * Input for right ImgFrame of left-right pair
     *
     * Default queue is non-blocking with size 8
     */
    Input right{*this, "right", Input::Type::SReceiver, false, 8, {{DatatypeEnum::ImgFrame, true}}};

    /**
     * Outputs ImgFrame message that carries RAW16 encoded (0..65535) depth data in millimeters.
     */
    Output depth{*this, "depth", Output::Type::MSender, {{DatatypeEnum::ImgFrame, false}}};

    /**
     * Outputs ImgFrame message that carries RAW8 encoded (0..96 or 0..192 for Extended mode) disparity data.
     */
    Output disparity{*this, "disparity", Output::Type::MSender, {{DatatypeEnum::ImgFrame, false}}};

    /**
     * Passthrough ImgFrame message from 'left' Input.
     */
    Output syncedLeft{*this, "syncedLeft", Output::Type::MSender, {{DatatypeEnum::ImgFrame, false}}};

    /**
     * Passthrough ImgFrame message from 'right' Input.
     */
    Output syncedRight{*this, "syncedRight", Output::Type::MSender, {{DatatypeEnum::ImgFrame, false}}};

    /**
     * Outputs ImgFrame message that carries RAW8 encoded (grayscale) rectified frame data.
     */
    Output rectifiedLeft{*this, "rectifiedLeft", Output::Type::MSender, {{DatatypeEnum::ImgFrame, false}}};

    /**
     * Outputs ImgFrame message that carries RAW8 encoded (grayscale) rectified frame data.
     */
    Output rectifiedRight{*this, "rectifiedRight", Output::Type::MSender, {{DatatypeEnum::ImgFrame, false}}};

    /**
     * Specify local filesystem path to the calibration file
     * @param path Path to calibration file. If empty use EEPROM
     */
    void loadCalibrationFile(const std::string& path);

    /**
     * Specify calibration data as a vector of bytes
     * @param path Calibration data. If empty use EEPROM
     */
    void loadCalibrationData(const std::vector<std::uint8_t>& data);

    /**
     * Specify that a passthrough/dummy calibration should be used,
     * when input frames are already rectified (e.g. sourced from recordings on the host)
     */
    void setEmptyCalibration();

    /**
     * Specify input resolution size
     *
     * Optional if MonoCamera exists, otherwise necessary
     */
    void setInputResolution(int width, int height);

    /**
     * @param median Set kernel size for disparity/depth median filtering, or disable
     */
    void setMedianFilter(Properties::MedianFilter median);

    /**
     * Confidence threshold for disparity calculation
     * @param confThr Confidence threshold value 0..255
     */
    void setConfidenceThreshold(int confThr);

    /**
     * Computes and combines disparities in both L-R and R-L directions, and combine them.
     *
     * For better occlusion handling
     */
    void setLeftRightCheck(bool enable);

    /**
     * Computes disparity with sub-pixel interpolation (5 fractional bits).
     *
     * Suitable for long range
     */
    void setSubpixel(bool enable);

    /**
     * Disparity range increased from 96 to 192, combined from full resolution and downscaled images.
     *
     * Suitable for short range objects
     */
    void setExtendedDisparity(bool enable);

    /**
     * Fill color for missing data at frame edges
     * @param color Grayscale 0..255, or -1 to replicate pixels
     */
    void setRectifyEdgeFillColor(int color);

    /**
     * Mirror rectified frames
     * @param enable True for normal disparity/depth, otherwise mirrored
     */
    void setRectifyMirrorFrame(bool enable);

    /**
     * Enable outputting rectified frames. Optimizes computation on device side when disabled
     */
    void setOutputRectified(bool enable);

    /**
     * Enable outputting 'depth' stream (converted from disparity).
     * In certain configurations, this will disable 'disparity' stream
     */
    void setOutputDepth(bool enable);
};

}  // namespace node
}  // namespace dai
