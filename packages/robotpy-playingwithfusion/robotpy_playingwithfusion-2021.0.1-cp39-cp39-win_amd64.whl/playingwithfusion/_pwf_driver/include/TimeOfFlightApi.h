#ifndef TIMEOFFLIGHTAPI_H
#define TIMEOFFLIGHTAPI_H

#include <stdint.h>
#include "TimeOfFlightApiTypes.h"

#ifdef __cplusplus
extern "C" {
#endif

struct TimeOfFlight_s;
typedef struct TimeOfFlight_s TimeOfFlight_t;

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
 *
 * @return Pointer to the TimeOfFlight instance
 */
TimeOfFlight_t *TimeOfFlight_Create(uint8_t sensorID);

/**
 * Destroy the TimeOfFlight object and free any asscioated resources
 * 
 * @param pHandle Pointer to the TimeOfFlight instance
 */
void TimeOfFlight_Destroy(TimeOfFlight_t *pHandle);

/**
 * Flash the time of flight sensor LED red and green 
 * to idicate the sensor asscioated with this instance
 * of software
 * 
 * @param pHandle Pointer to the TimeOfFlight instance
 */
void TimeOfFlight_IdentifySensor(TimeOfFlight_t *pHandle);

/**
 * Determine the sensor firmware version
 * 
 * @param pHandle Pointer to the TimeOfFlight instance
 *
 * @return The sensor firmware version
 */
uint32_t TimeOfFlight_GetFirmwareVersion(TimeOfFlight_t *pHandle);

/**
 * Determine the sensor hardware serial number
 * 
 * @param pHandle Pointer to the TimeOfFlight instance
 *
 * @return The sensor hardware serial number
 */
uint32_t TimeOfFlight_GetSerialNumber(TimeOfFlight_t *pHandle);

/**
 * Determine if the last measurment was valid
 * 
 * @param pHandle Pointer to the TimeOfFlight instance
 *
 * @return TRUE if the Time Of Flight Sensor sucessfully measured distance to an object
 */
uint8_t TimeOfFlight_IsRangeValid(TimeOfFlight_t *pHandle);

/**
 * Get the distance between the sensor and the target
 *
 * @param pHandle Pointer to the TimeOfFlight instance
 * 
 * @return Distance to target in millimeters
 */
double TimeOfFlight_GetRange(TimeOfFlight_t *pHandle);

/**
 * Get the standard deviation of the distance measurment in millimeters
 *
 * @param pHandle Pointer to the TimeOfFlight instance
 * 
 * @return Standard deviation of distance measurment in millimeters
 */
double TimeOfFlight_GetRangeSigma(TimeOfFlight_t *pHandle);

/**
 * Get ambient lighting level in mega counts per second.
 *
 * @param pHandle Pointer to the TimeOfFlight instance
 * 
 * @return Ambient lighting level in mega counts per second.
 */
double TimeOfFlight_GetAmbientLightLevel(TimeOfFlight_t *pHandle);

/**
 * Get status of the last distance measurement.
 *
 * @param pHandle Pointer to the TimeOfFlight instance
 * 
 * @return Status of last measurement.  See VL53L1X datasheet for more details
 */
TimeOfFlight_Status TimeOfFlight_GetStatus(TimeOfFlight_t *pHandle);

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
 * @param pHandle    Pointer to the TimeOfFlight instance
 * @param mode       The desired sensor ranging mode (short, medium, long)
 * @param sampleTime The desired sample time in milliseconds
 */
void TimeOfFlight_SetRangingMode(TimeOfFlight_t *pHandle, TimeOfFlight_RangingMode mode, double sampleTime);

/**
 * Get the sensor sampling period in milliseconds
 *
 * @param pHandle Pointer to the TimeOfFlight instance
 * 
 * @return Sensor sampling period in milliseconds
 */
double TimeOfFlight_GetSampleTime(TimeOfFlight_t *pHandle);

/**
 * Get the sensor ranging mode
 *
 * @param pHandle Pointer to the TimeOfFlight instance
 * 
 * @return Sensor ranging mode
 */
TimeOfFlight_RangingMode TimeOfFlight_GetRangingMode(TimeOfFlight_t *pHandle);

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
 * @param pHandle Pointer to the TimeOfFlight instance
 * @param topLeftX Column of the top left corner of the region of interest.
 * @param topLeftY Row of the top left corner of the region of interest. 
 * @param bottomRightX Column of the bottom right corner of the region of interest. 
 * @param bottomRightY Row of the bottom right corner of the region of interest.
 */
void TimeOfFlight_SetRangeOfInterest(TimeOfFlight_t *pHandle, uint8_t topLeftX, uint8_t topLeftY, uint8_t bottomRightX, uint8_t bottomRightY);

#ifdef __cplusplus
}
#endif

#endif // TIMEOFFLIGHTAPI_H