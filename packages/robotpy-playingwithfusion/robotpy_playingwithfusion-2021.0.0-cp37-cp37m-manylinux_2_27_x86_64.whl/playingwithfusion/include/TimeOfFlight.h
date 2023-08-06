#pragma once

#include "frc/PIDSource.h"
#include "frc/smartdashboard/SendableBase.h"
#include "frc/smartdashboard/SendableBuilder.h"
#include "TimeOfFlightApi.h"

namespace frc {
class TimeOfFlightImpl;

class TimeOfFlight : public PIDSource, public SendableBase {
public:
    enum RangingMode {
        kShort   = 0,
        kMedium  = 1,
        kLong    = 2
    };

    enum Status {
        /**
         * Measured distance is valid
         */
        kValid = 0,

        /**
         * Sigma estimator check is above internally defined threshold.   The repeatability
         * or standard deviation of the measurement is bad due to a decreasing signal noise
         * ratio. Increasing the timing budget can improve the standard deviation.
         */
        kSigmaHigh = 1,

        /**
         * Return signal value is below the internal defined threshold.  The return signal is
         * too week to return a good answer. The target may be too far, not reflective enough,
         * or too small. Increasing the timing buget might help, but there may simply be no 
         * target available.
         */
        kReturnSignalLow = 2,

        /**
         * Return signal phase is out of bounds.   This means that the sensor is ranging in a 
         * "nonappropriated" zone and the measured result may be inconsistent. This status is
         * considered as a warning but, in general, it happens when a target is at the maximum 
         * distance possible from the sensor.
         */
        kReturnPhaseBad = 4,

        /**
         * Hardware failure
         */
        kHardwareFailure = 5,

        /**
         * Wrapped target, non-matching phases.   This situation may occur when the target is 
         * very reflective and the distance to the target/sensor is longer than the physical 
         * limited distance measurable by the sensor. For example, approximately 5m when the senor
         * is in Long distance mode and approximately 1.3 m when the sensor is in Short distance
         * mode.
         */
        kWrappedTarget = 7,

        /**
         * Internal algorithm underflow or overflow
         */
        kInternalError = 8,

        /**
         * The measured distance is invalid
         */
        kInvalid = 14
    };


    /**
     * Create an instance of the CAN Time Of Flight sensor.
     *
     * This is designed to support the Playing With Fusion (PWF) SEN-36005 time of
     * flight sensor
     *
     * @param sensorID The 6-bit identifier used to select a particular
     *                 sensor on the CAN bus.  This identifier may be set
     *                 through the PWF Device configuration page on the 
     *                 roboRIO.
     */
    explicit TimeOfFlight(uint8_t sensorID);
    virtual ~TimeOfFlight();

    // Delete Copy constructor and assignment operator
    TimeOfFlight(const TimeOfFlight&) =delete;
    TimeOfFlight& operator=(const TimeOfFlight&) =delete;

    // Use default Move constructor and assignment operator
    TimeOfFlight(TimeOfFlight&&) =default;
    TimeOfFlight& operator=(TimeOfFlight&&) =default;

    /**
     * Flash the time of flight sensor LED red and green 
     * to idicate the sensor asscioated with this instance
     * of software
     */
    void IdentifySensor();

    /**
     * Determine the sensor firmware version
     *
     * @return The sensor firmware version
     */
    uint32_t GetFirmwareVersion() const;

    /**
     * Determine the sensor hardware serial number
     *
     * @return The sensor hardware serial number
     */
    uint32_t GetSerialNumber() const;

    /**
     * Determine if the last measurment was valid
     *
     * @return TRUE if the Time Of Flight Sensor sucessfully measured distance to an object
     */
    bool IsRangeValid() const;

    /**
     * Get the distance between the sensor and the target
     *
     * @return Distance to target in millimeters
     */
    double GetRange() const;

    /**
     * Get the standard deviation of the distance measurment in millimeters
     *
     * @return Standard deviation of distance measurment in millimeters
     */
    double GetRangeSigma() const;

    /**
     * Get ambient lighting level in mega counts per second.
     *
     * @return Ambient lighting level in mega counts per second.
     */
    double GetAmbientLightLevel() const;

    /**
     * Get status of the last distance measurement.
     *
     * @return Status of last measurement.  See VL53L1X datasheet for more details
     */
    Status GetStatus() const;

    /**
     * Configure the ranging mode as well as the sample rate of the time
     * of flight sensor
     * 
     * The ranging mode specifies the trade off between maximum measure distance
     * verses reliablity in bright situations.  Short mode (default) works the best
     * in bright lighting conditions, but can only measure 1.3 meters.   Long mode
     * can measure up to 4 meters in the dark, but may only be able to measure
     * shorter distances depending on the lighting conditions.  See the Vl53L1x 
     * datasheet for more information
     * 
     * The sample time specifies the how frequently the time of flight sensor attempts
     * to measure the distance to a target.  The sample time must be between 24 and
     * 1000 milliseconds.
     *
     * @param mode       The desired sensor ranging mode (short, medium, long)
     * @param sampleTime The desired sample time in milliseconds
     */
    void SetRangingMode(RangingMode mode, double sampleTime);

    /**
     * Specify the region of the imaging sensor used for range measurement.
     * 
     * <p>The region of interest refers to the pixels within the time of flight imaging sensor
     * that are used to detect reflected laser light form the target.  The sensor contains
     * a 16x16 pixel grid.   By default, all 256 pixels are used which results in a roughly
     * 27 degree field of view.
     * 
     * <p>The Field of view refers to a cone which grows from the time of flight sensor outward.
     * By reducing the size of the region of interest (by using a smaller area of pixels) it is
     * possible to reduce the field of view.  This can be helpfull when measuring objects far
     * away.  The smaller the field of view, the smaller the area where the sensor can detect 
     * targets.
     * 
     * <p>Reducing the region of interest will reduce the sensitivity of the sensor.  It may be 
     * necessary to increase the reflectivity of the target or to increase the sample time to 
     * compensate.
     * 
     * <p>The range of interest rows and columns must be greater or equal to zero and less than
     * or equal to fifteen.   The top left corner row/column must be smaller than the bottom
     * right column/row.  The region of interest must be at least four coulmns wide and four
     * rows tall.   For example, to specify a 4x4 region at the center of the image sensor use:
     * 
     * <p>TimeOfFlight_SetRangeOfInterest(pHandle, 8, 8, 12, 12);
     * 
     * @param topLeftX Column of the top left corner of the region of interest.
     * @param topLeftY Row of the top left corner of the region of interest. 
     * @param bottomRightX Column of the bottom right corner of the region of interest. 
     * @param bottomRightY Row of the bottom right corner of the region of interest.
     */
    void SetRangeOfInterest(uint8_t topLeftX, uint8_t topLeftY, uint8_t bottomRightX, uint8_t bottomRightY);

    /**
     * Get the range in millimeters for the PIDSource base object.
     *
     * @return The range in millimeters
     */
    double PIDGet() override;

    void SetPIDSourceType(PIDSourceType pidSource) override;

    void InitSendable(SendableBuilder& builder) override;

private:
   TimeOfFlight_t *m_timeOfFlightHandle;
   RangingMode m_rangingMode;
};

}