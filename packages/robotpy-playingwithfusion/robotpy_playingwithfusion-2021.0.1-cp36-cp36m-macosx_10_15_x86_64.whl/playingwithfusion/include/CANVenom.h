#pragma once

#include "frc/MotorSafety.h"
#include "frc/SpeedController.h"
#include "frc/smartdashboard/SendableBase.h"
#include "frc/smartdashboard/SendableBuilder.h"
#include "CANVenomApi.h"

namespace frc {
class CANVenomImpl;

    /**
     * CAN based Venom motor controller instance
     *
     * <p>This class is used to control a single Venom motor connected to the roboRIO
     * through the CAN bus.  The motor supports many controls modes, including:
     * Proportional Dutycycle, Voltage compensated proportional, closed-loop current,
     * closed-loop speed with true s-curve trajector planning, closed-loop position
     * control and motion profile execution
     */
class CANVenom : public MotorSafety, public SpeedController, public SendableBase {
  public:
    enum ControlMode {
        /** 
          * Motor is disabled and coasting
          */
        kDisabled = 0,

        /**
          * Proportional (duty-cycle) control
          */
        kProportional = 1,

        /** Closed-loop current (torque) control
          * 
          */
        kCurrentControl = 3,
    
        /**
          * Closed-loop speed control.
          */
        kSpeedControl = 4,

        /**
          * Closed-loop position (servo) control.
          */
        kPositionControl = 5,

        /**
          * Execute a motion control path.  
          * 
          * Motion profiles are generally
          * loaded in Disabled mode.  The transition to the MotionProfile
          * state causes Venom to begin following the path.
          */
        kMotionProfile = 6,

        /** 
          * Follow the duty cycle commanded to another Venom motor.   
          * 
          * Generally
          * used when more that one Venom is geared together in a drivetrain 
          * application.  In that case one Venom, the leader, executes a motion 
          * profile or is placed in another control mode.  The other Venom(s) 
          * are placed in FolloewTheLeader and command the same duty cycle as 
          * the leader so that only the leader is used to calculate closed-loop 
          * commands.  This avoid implementing PID controllers on multiple motors 
          * which may "fight".
          */
        kFollowTheLeader = 7,

        /**
          * Open-loop voltage control mode, also refered to voltage compensated
          * proportional mode
          */
        kVoltageControl = 8
    };

    enum BrakeCoastMode {
        /**
          * The motor is open circuited when the porportional or volatage command
          * is zero, causing the motor to coast or free-wheel
          */
        kCoast = 0,

        /**
          * The motor is shorted when the porportional or vlotage command is zero.  
          * This acts to brake/slow the motor to a stop.
          */
        kBrake = 1
    };

    enum FaultFlag {
        /**
         * No Active Faults
         */
        kNone = 0,

        /**
         * Missing heartbeat from the roboRIO.  Ensure device ID matches device ID
         * used by CANVenom class.
         */
        kNoHeartbeat = 1,

        /**
         * Lead motor heartbeat is missing while in FollowTheLeader mode.
         */
        kNoLeaderHeartbeat = 2,

        /**
         * The lead motor ID is same as the motor ID.   One Venom cannot follow itself.
         * Ensure the leader and follower have different IDs
         */
        kBadLeaderID = 4,

        /**
         * Motor temperature is too high
         */
        kHighTemperature = 8,

        /**
         * Average motor current is too high
         */
        kHighCurrent = 16,

        /**
         * An invalid control mode was specified by the roboRIO.   This should not
         * occur when using PlayingWithFusionDriver.  Contact PWF Technical support.
         */
        kBadMode = 32,

        /**
         * Another Venom with the same device ID was detected on the CAN bus.  All
         * Venom device IDs must be unique
         */
        kDuplicateID = 64,

        /**
         * The forward limit switch is enabled and is active
         */
        kForwardLimit = 128,

        /**
         * The reverse limit switch is enabled and is active
         */
        kReverseLimit = 256,

        /**
         * The Venom motor reset, lost power, or browned out since the last time
         * the {@link #ClearLatchedFaults} function was called
         */
        kReset = 512
    };


    enum MotionProfileState {
        /**
         * Initial state after Venom powerup
         */
        kInit = 0,

        /**
         * Motion profile is currently executing, but has not reached the final
         * point yet.  No errors are active
         */
        kRunning = 1,

        /**
         * The motion profile buffer was cleared while the profile was being
         * executed.  The motor cannot continue and will coast until the motor
         * is placed in another control mode (to reset the error condition)
         */
        kErrBufferCleared = 2,

        /**
         * The motor ran out of points while executing a motion profile.  Either
         * new points were not sent to the motor fast enough or the profile wasn't
         * terminated using the {@link #CompleteMotionProfilePath} function.
         * The motor cannot continue and will coast until the motor is placed 
         * in another control mode (to reset the error condition)
         */
        kErrBufferUnderflow = 3,

        /**
         * Attempted to begin executing a motion profile but there was no valid
         * start point.  This can happen if the {@link #ClearMotionProfilePoints} 
         * function is not called before loading a motion profile, or if too many
         * points are loaded and the motor cannot buffer the entire path.
         * 
         * <p>Venom can buffer about 300 points.  The exact buffer length can be
         * be determined by calling {@link #GetNumAvaliableMotionProfilePoints}
         * immediatly after power up.  If the motion profile contains more points
         * than can be stored in the buffer, the profile must be reloaded each time
         * before begining to follow the profile.
         * 
         * <p>For large paths with many points, first load a subset of the points,
         * begin executing the path, then continue to load new points as the motor
         * executes the path.   Call the {@link #GetNumAvaliableMotionProfilePoints}
         * function periodically to ensure the Venom buffer has sufficient space
         * before loading additional points.
         */
        kErrBufferInvalid = 4,

        /**
         * The motion profile was successfully executed.  The motor will now
         * hold the current position (at zero speed) until the motor is placed
         * in another control mode.
         */
        kDone = 5
    };


    /**
     * Create an instance of the CAN Venom Motor Controller driver.
     *
     * This is designed to support the Playing With Fusion Venom motor
     * controller
     *
     * @param motorId The 6-bit identifier used to select a particular
     *                 motor on the CAN bus.  This identifier may be set
     *                 through the PWF Device configuration page on the 
     *                 roboRIO.
     */
    explicit CANVenom(uint8_t motorID);
    /**
     * Destroy the CANVenom object and free any asscioated resources.
     */
    virtual ~CANVenom();

    // Delete Copy constructor and assignment operator
    CANVenom(const CANVenom&) =delete;
    CANVenom& operator=(const CANVenom&) =delete;

    // Use default Move constructor and assignment operator
    CANVenom(CANVenom&&) =default;
    CANVenom& operator=(CANVenom&&) =default;


    /**
     * Stop applying power to the motor immediately.  
     * 
     * If Brake mode is active and the current control mode is Proportional
     * or VoltageControl the motor will brake to a stop.  Otherwise the
     * motor will coast.
     * 
     * The enable() function must be called after a call to stopMotor()
     * before motion may be commanded again.  
     */
    virtual void StopMotor() override;


    /**
     * Return a description of this motor controller.
     * 
     * @return The Venom motor controller description
     */
    virtual void GetDescription(wpi::raw_ostream& desc) const override;


    /**
     * Sets the motor duty-cycle command.
     *
     * <p>Places the motor in Proportional control mode and sets the motor
     * proportional command.   If disable() or stopMotor() is 
     * called, enable() must be called before set() will command motion
     * again.
     *
     * @param speed Proportional motor duty-cycle command from -1.0 to 1.0
     */
    virtual void Set(double command) override;


    /**
     * Get the motor duty-cycle.
     * 
     * @return The motor duty cycle as a ratio between -1.0 and 1.0.
     */
    virtual double Get() const override;


    /**
     * Specify which direction the motor rotates in response to a posive 
     * motor command.
     * 
     * <p>When inverted the motor will spin the opposite direction it rotates
     * when isInverted is false.  The motor will always report a positive
     * speed when commanded in the 'forward' direction.
     * 
     * <p>This function is commonly used for drivetrain applications so that the
     * and right motors both drive the frobot forward when given a forward 
     * command, even though one side is spinnig clockwise and the other is
     * spinning counter clockwise.
     * 
     * @param isInverted True if the motor direction should be reversed
     */
    virtual void SetInverted(bool isInverted) override;


    /** 
     * Return the motor direction inversion state.
     * 
     * @return True if the motor direction is inverted
     */
    virtual bool GetInverted() const override;


    /**
     * Stop applying power to the motor immediately.  
     * 
     * <p>If Brake mode is active and the current control mode is Proportional 
     * or VoltageControl the motor will brake to a stop.  Otherwise the
     * motor will coast.
     * 
     * <p>The enable() function must be called after a call to stopMotor()
     * before motion may be commanded again.
     */
    virtual void Disable() override;
	
	
    /**
     * Enable the motor again after a call to stopMotor() or disable().
     */
    void Enable();


    /**
     * Used by an instance of PIDController to command the motor 
     * duty-cycle
     *
     * <p>Places the motor in Proportional control mode and sets the motor 
     * proportional command.   If disable() or stopMotor() is 
     * called, enable() must be called before set() will command motion
     * again.
     *
     * @param speed Proportional motor command from -1.0 to 1.0
     */
    virtual void PIDWrite(double output) override;

	
    /**
     * Initialize vaiiables and parameters to be passed into the
     * smart dashboard.
     */
    virtual void InitSendable (SendableBuilder &builder) override;


    /**
     * Set the motor command and control mode.
     * 
     * <p>Where control mode is one of:
     * <p><ul>
     * <li>Proportional - command specifies the raw motor duty-cycle as a ratio between -1.0 and 1.0
     * <li>CurrentControl - command specifies a target motor current in Amps between -40.0 and 40.0.
     *        <ul><li>Note that the commanded is signed to specify the motor direction, but the measured motor
     *        current provided by the getOutputCurrent() function is unsigned (the absolute value of current)
     *        <li>In this mode a PID active controls the motor duty cycle to achieve the commanded current.</ul>
     * <li>VoltageControl - command specified the voltage to be applied to the motor bushes as a value
     *        between 0.0 and 14.0 Volts.  <ul><li>This mode is also refered to as voltage compensated proportional
     *        mode.  <li>Is is useful because the motor speed at a given voltage voltage will be constant if the 
     *        battery voltage changes, as long as the voltage command is less than the battery voltage.</ul>
     * <li>SpeedControl - command specifies the motor speed value between -6000.0 and 6000.0 RPM.  <ul><li>In this
     *        mode a PID activle controls the motor duty cycle to achieve the commanded speed</ul>
     * <li>PositionControl - command specifies the motor position as a value between -4096 and 4096 motor
     *        revolutions.  <ul><li>This mode is sometime refered to as servo control because the motor attempts to
     *        hold a commanded position, just like a servo.   <li>In this mode a PID actively controls motor
     *        duty cycle to achieve the commanded position</li></ul>
     * <li>MotionProfile - command is unused. 
     *        <ul><li>The motor attempts to follow a previously entered motion profile.  <li>Once the last point in the
     *        motion profile is reached the motor will hold the last command position from the profile. 
     *        <li>See the addMotionProfilePoint() function for more details</ul>
     * <li>FollowTheLeader - command specified the device ID of the Venom motor to follow.
     *        <ul><li>In this mode the Venom motor will command the same duty cycle as the lead motor.
     *        <li>Generally used when more that one Venom is geared together in a drivetrain 
     *        application.  In that case one Venom, the leader, executes a motion 
     *        profile or is placed in another control mode.  The other Venom(s) 
     *        are placed in FolloewTheLeader and command the same duty cycle as 
     *        the leader so that only the leader is used to calculate closed-loop 
     *        commands.  This avoid implementing PID controllers on multiple motors which may "fight".</ul>
     *        </ul>
     * @param mode Motor control mode (Proportional, CurrentControl, SpeedControl, etc.)
     * @param command Motor command (%, Amps, RPM, etc)
     */
    void SetCommand(ControlMode mode, double command);


    /**
     * Set the motor command and control mode.
     * 
     * <p>Where control mode is one of:
     * <p><ul>
     * <li>Proportional - command specifies the raw motor duty-cycle as a ratio between -1.0 and 1.0
     * <li>CurrentControl - command specifies a target motor current in Amps between -40.0 and 40.0.
     *        <ul><li>Note that the commanded is signed to specify the motor direction, but the measured motor
     *        current provided by the getOutputCurrent() function is unsigned (the absolute value of current)
     *        <li>In this mode a PID active controls the motor duty cycle to achieve the commanded current.</ul>
     * <li>VoltageControl - command specified the voltage to be applied to the motor bushes as a value
     *        between 0.0 and 14.0 Volts.  <ul><li>This mode is also refered to as voltage compensated proportional
     *        mode.  <li>Is is useful because the motor speed at a given voltage voltage will be constant if the 
     *        battery voltage changes, as long as the voltage command is less than the battery voltage.</ul>
     * <li>SpeedControl - command specifies the motor speed value between -6000.0 and 6000.0 RPM.  <ul><li>In this
     *        mode a PID activle controls the motor duty cycle to achieve the commanded speed</ul>
     * <li>PositionControl - command specifies the motor position as a value between -4096 and 4096 motor
     *        revolutions.  <ul><li>This mode is sometime refered to as servo control because the motor attempts to
     *        hold a commanded position, just like a servo.   <li>In this mode a PID actively controls motor
     *        duty cycle to achieve the commanded position</li></ul>
     * <li>MotionProfile - command is unused. 
     *        <ul><li>The motor attempts to follow a previously entered motion profile.  <li>Once the last point in the
     *        motion profile is reached the motor will hold the last command position from the profile. 
     *        <li>See the {@link #AddMotionProfilePoint} function for more details</ul>
     * <li>FollowTheLeader - command specified the device ID of the Venom motor to follow.
     *        <ul><li>In this mode the Venom motor will command the same duty cycle as the lead motor.
     *        <li>Generally used when more that one Venom is geared together in a drivetrain 
     *        application.  In that case one Venom, the leader, executes a motion 
     *        profile or is placed in another control mode.  The other Venom(s) 
     *        are placed in FolloewTheLeader and command the same duty cycle as 
     *        the leader so that only the leader is used to calculate closed-loop 
     *        commands.  This avoid implementing PID controllers on multiple motors which may "fight".</ul>
     *        </ul>
     * <p>When the kF and b terms are included in this function, they are guarenteed to be sent to the
     * motor in the same CAN frame as the control mode and command.   This is useful when an open-loop
     * correction or feed-forward term is calculated by the roboRIO.
     * 
     * @param mode Motor control mode (Proportional, CurrentControl, SpeedControl, etc.)
     * @param command Motor command (%, Amps, RPM, etc)
     * @param kF Feed-forward gain as ratio between -8.0 and 8.0
     * @param b Feed-forward offset as duty-cycle between -2.0 and 2.0
     */
    void SetCommand(ControlMode mode, double command, double kF, double b);
  

    /**
     * Place the motor into FollowTheLeader mode and follow the specified motor
     * 
     * <p>This method is equivelent to calling SetComand(FollowTheLeader, ID_of_lead_motor);
     * 
     * @param leadVenom Reference to the CANVenom instance which reperesents the lead motor.
     */
    void Follow(CANVenom &leadVenom);


    /**
     * Determine the state of the forward motion limit switch.
     * 
     * <p>An internal pull-up resistor activates the limit switch is nothing
     * is connected.  Connect the limit switch to GND to deactivate the limit.
     * 
     * @return true if the limit switch voltage is high (which would prevent
     *        forward rotation if the limit was enabled)
     */
    bool GetFwdLimitSwitchActive() const;
	

	    /**
     * Determine the state of the reverse motion limit switch.
     * 
     * <p>And internal pull-up resistor activates the limit switch is nothing
     * is connected.  Connect the limit switch to GND to deactivate the limit.
     * 
     * @return true if the limit switch voltage is high (which would prevent
     *        reverse rotation if the limit was enabled)
     */
    bool GetRevLimitSwitchActive() const;
	
	
    /**
     * Enable/disable the forward and reverse limit switches.
     * 
     * @param fwdLimitSwitchEnabled Prevent forward rotation if this argument
     *        is true and the forward limit switch is active
     * 
     * @param revLimitSwitchEnabled Prevent reverse rotation if this argument
     *        is true and the forward limit switch is active
     */
    void EnableLimitSwitches(bool fwdLimitSwitchEnabled, bool revLimitSwitchEnabled);


    /**
     * Flash LED to identify motor.
     * 
     * <p>Identify the physical motor asscioated with this instance of the
     * Venom driver by causing its LED to flash red and green for several
     * seconds.
     */
    void IdentifyMotor();


    /**
     * Reset the motor revolution counter (position) to 0.
     */
    void ResetPosition();

    /**
     * Reset the motor revolution counter (position) to the specified position.
     * 
     * @param newPosition Value to assign motor position in revolutions
     */
    void SetPosition(double newPosition);

    /**
     * Get number of empty motion profile points avaliable. 
     *
     * <p>Gets number of motion profile point buffer locations avaliable in motor controller.
     * The motor will ignore additional calls to addMotionProfilePoint() once all
     * buffer locations are full.
     * 
     * @return The number of remaining empty motion profile points which may be loaded into the Venom controller
     */
    uint16_t GetNumAvaliableMotionProfilePoints() const;


    /**
     * Get current motion profile point 
     *
     * <p>Gets the active motion profile point while a motion profile is active.  The first point
     * sent to the controller acter a call to clearMotionProfilePoints() is point 0.  The next point
     * is 1, then 2, and so on.
     * 
     * @return The motion profile point which is currently targeted by the Venom controller
     */
    uint16_t GetCurrentMotionProfilePoint() const;


    /**
     * Get the instantaneous motion profile position commanded
     *
     * <p>Gets the motor position commanded by the current motion profile point
     * while a motion profile is active
     * 
     * @return The commanded motor position in revolutions.
     */
    double GetMotionProfilePositionTarget() const;


    /**
     * Get the instantaneous motion profile speed commanded
     *
     * <p>Gets the motor speed commanded by the current motion profile point
     * while a motion profile is active
     * 
     * @return The commanded speed position in revolutions per second (not RPM).
     */
    double GetMotionProfileSpeedTarget() const;


    /**
     * Determine if the motor is prepared to execute a motion profile
     *
     * <p>Determins is a valit start point is present and that the motor is read
     * to begin executing a motion profile. 
     * 
     * @return True if the motion profile stored on the motor contains a valid start point
     */
    bool GetMotionProfileIsValid() const;

    /**
     * Get the Motion Profile state.
     *
     * <p>Gets the state of the internal Venom Motion Profile state machine.
     * This state can be used to determine if a motion profile is being executed,
     * has completed sucessfully, or has stopped due to an error.
     * 
     * @return Venom Motion Profile state.
     */
    MotionProfileState GetMotionProfileState() const;

    /**
     * Erase all motion profile points. 
     *
     * <p>Clear all motion profile points from the motor controller buffer.  This function should
     * Be called first, each time a new motion profile path is loaded into the motor controller.
     */
    void ClearMotionProfilePoints();


    /**
     * Add single motion profile point.
     *
     * <p>Add a single point to the motion profile buffer.   To load a motion profile, the application
     * should call clearMotionProfilePoints(), then call addMotionProfilePoint()
     * for each point.  The application should then close the path using completeMotionProfilePath()
     * Once a path is loaded, or partially loaded, the application may initiate the motion profile
     * using executePath() or setCommand(ControlMode.MotionProfile, 0)
     * 
     * <p>The motor will will lineraly interpolate commanded speed and position between motion profile
     * points.   Acceleration and Jerk limits are not used when executing a motion profile
     *
     * @param time Time since the start of the profile in miliseconds
     * @param speed Commanded speed in rotations per second
     * @param position Commanded motor angle/position in revolutions
     */
    void AddMotionProfilePoint(double time, double speed, double position);


    /**
     * Add final point to motion profile.
     *
     * <p>Add the last point to a motion profile.  The motor will attempt to hold the commanded poistion
     * indefinitly once reaching the final point. 
     *
     * @param time Time since the start of the profile in milliseconds
     * @param position Commanded motor angle/position in revolution
     */
    void CompleteMotionProfilePath(double time, double position);


    /**
     * Execute stored motion profile.
     *
     * <p>Instruct the motor to begin following the sotred motion profile.  This
     * function is equivlelent to calling setCommand(ControlMode.MotionProfile, 0)
     */
    void ExecutePath();


    /**
     * Return the Venom motor firmware version of the motor
     * asscioated with this instance of the CANVenom class.
     * 
     * @return The Venom motor firmware version (multiplied by 100)
     */
    uint32_t GetFirmwareVersion() const;


    /**
     * Return the serial number of the motor asscioated with this
     * instance of the CANVenom class.
     * 
     * @return The Venom motor serial number
     */
    uint32_t GetSerialNumber() const;


    /**
     * Get the bus (battery) voltage supplying the Venmom motor.
     * 
     * @return The bus voltage in Volts
     */
    double GetBusVoltage() const;


    /**
     * Get the calculated voltage across the motor burshes.
     * 
     * @return The calculated motor voltage in Volts.
     */
    double GetOutputVoltage() const;


    /**
     * Get the motor h-bridge duty cycle.
     * 
     * @return The motor duty cycle as a ration between -1.0 and 1.0
     */
    double GetDutyCycle() const;


    /**
     * Get the measured motor current consumption.
     * 
     * <p>Current is measured between the Venom power leads (the battery) to the
     * motor brushes.   Current is positive regardles of motor direction.  Only
     * current from the battery to the motor is measured.   Zero amps are returned
     * if the motor is charging the battery.
     * 
     * @return The measured current Amps.
     */
    double GetOutputCurrent() const;


    /**
     * The measured Venom backplate temperature.
     * 
     * @return Measured backplate temperature in degrees C.
     */
    double GetTemperature() const;


    /**
     * Get the measured voltage at the auxilary analog input on the limit
     * switch breakout board.
     * 
     * @return Auxilary analog input voltage in Volts.
     */
    double GetAuxVoltage() const;


    /**
     * Measured signed motor velocity in RPM.
     * 
     * @return Motor velocity in RPM.
     */
    double GetSpeed() const;


    /**
     * Signed motor revolutions (position) since the last time it was cleared.
     * 
     * @return The signed motor position in revolutions.
     */
    double GetPosition() const;


    /**
     * Internal PID Target (position, speed, current).
     * 
     * <p>The PID target is equal to the motor command specified by setCommand() in CurrentControl mode.
     * In SpeedControl and PositionControl modes, the PID command is the output of the s-curve or trapezoidal
     * slew rate limit calculation.  In MotionProfile mode the PID command is equal to the current
     * motion profile position command.
     * 
     * <p>In all closed-loop modes, the PID target represents the motor speed/position/current that the
     * Venom PID is activly trying to achieve
     * 
     * @return PID target in RPM, rotations, or Amps (based on current control mode)
     */
    double GetPIDTarget() const;


    /**
     * Get the feed-forward gain in SpeedControl, PositionControl, CurrentCurrent
     * and MotionProfile control modes.
     * 
     * @return Feed-forward gain as ratio between -8.0 and 8.0.
     */
    double GetKF() const;


    /**
     * Get the feed-forward command offset in SpeedControl, PositionControl,
     * CurrentCurrent and MotionProfile control modes.
     * 
     * @return Feed-forward offset as duty-cycle between -2.0 and 2.0.
     */
    double GetB() const;


    /**
     * Get the close-loop PID proportional gain in SpeedControl,
     * PositionControl, CurrentCurrent and MotionProfile control modes.
     * 
     * @return PID proportional gain as ratio between 0.0 and 4.0.
     */
    double GetKP() const;


    /**
     * Get the close-loop PID integral gain in SpeedControl,
     * PositionControl, CurrentCurrent and MotionProfile control modes.
     * 
     * @return PID integral gain as ratio between 0.0 and 4.0.
     */
    double GetKI() const;


    /**
     * Get the close-loop PID derative gain in SpeedControl,
     * PositionControl, CurrentCurrent and MotionProfile control modes.
     * 
     * @return PID derivative gain as ratio between 0.0 and 4.0.
     */
    double GetKD() const;


    /**
     * Get the minimum duty cycle that may be commanded by the PID in
     * SpeedControl, PositionControl, CurrentCurrent and MotionProfile
     * control modes.
     *  
     * @return Minimum PID output duty-cycle as a ratio between -1.0 and 1.0.
     */
    double GetMinPILimit() const;


    /**
     * Get the maximum duty cycle that may be commanded by the PID in
     * SpeedControl, PositionControl, CurrentCurrent and MotionProfile
     * control modes.
     *  
     * @return Maximum PID output duty-cycle as a ratio between -1.0 and 1.0.
     */
    double GetMaxPILimit() const;


     /**
     * Get the maximum speed (absolute value of velocity) that may be commanded
     * in the SpeedControl and PositionControl control modes.
     *  
     * @return Maximum speed command in RPM.
     */
    double GetMaxSpeed() const;


    /**
     * Get the maximum acceleration in the SpeedControl and PositionControl
     * control modes.  
     * 
     * <p>This number is used as part of the s-curve path planning
     * in SpeedControl mode and the trapezoid planning in Position Control
     * mode.
     * 
     * <p>Trajectory planning is disabled if the maximum accelleration is zero.
     *  
     * @return Maximum acceleration RPM per second
     */
    double GetMaxAcceleration() const;


    /**
     * Get the maximum jerk (second derivitive of speed) in the SpeedControl
     * control mode.  
     * 
     * <p>This number is used as part of the s-curve path planning.
     * 
     * <p>The jerk limit is disabled if the maximum jerk is 0..
     *
     * @return Maximum jerk RPM per second squared
     */
    double GetMaxJerk() const;


    /**
     * Get the commanded Venom control mode.
     * 
     * @return The commanded control mode
     */
    ControlMode GetControlMode() const;


    /**
     * Get the active Venom control mode.
     * 
     * @return Get the active Venom control mode reported by the motor.
     */
    ControlMode GetActiveControlMode() const;


    /**
     * Get the brake/coast behavior when zero is commanded in Proportional
     * and VoltageControl control modes.
     * 
     * @return The Brake or Coast behavion in Proportional and VoltageControl modes
     */
    BrakeCoastMode GetBrakeCoastMode() const;


    /**
     * Return set of active motor faults which curently limit or disable motor
     * output.   More than one Fault may be active at a time
     * 
     * @return Bitmask of active faults
     */
    FaultFlag GetActiveFaults() const;

    /**
     * Return set of latched motor faults which are curently active or
     * were previously active since the last time the 
     * {@link #ClearLatchedFaults} function was called.  This function can be
     * helpful when diagnosing harness or brownout issues which cause Venom
     * to reset.  The Reset flag will be set each time venom starts up.
     * 
     * @return Bitmask of latched faults
     */
    FaultFlag GetLatchedFaults() const;
    
    /**
     * Clear all latched faults
     */
    void ClearLatchedFaults();

    /** 
     * Set the PID gains for closed-loop control modes.
     * 
     * <p>Sets the proportional, integral, and derivative gains as well as
     * the feed-forward gain and offset.  In general, the motor duty-cycle
     * is calculated using:
     * 
     * <p>error = (commandedValue - measuredValue)
     * <p>dutyCycle = (kP * error) + (kI * integral(error)) + (kD * derrivative(error)) + (kF * commandedValue) + b
     * 
     * @param kP Proportional gain as a ratio between 0.0 and 4.0
     * @param kI Integral gain as a ratio between 0.0 and 4.0
     * @param kD Derivative gain as a ratio between 0.0 and 4.0
     * @param kF Feed-forward gain as a ratio between -2.0 and 2.0
     * @param b Feed-forward offset as duty-cycle between -2.0 and 2.0
     */
    void SetPID(double kP, double kI, double kD, double kF, double b);


    /**
     * Set Feed-forward gain in closed loop control modes.
     * 
     * @param kF Feed-forward gain as a ratio between -2.0 and 2.0
     */
    void SetKF(double kF);


    /**
     * Set Feed-forward duty cycle offset in closed loop control modes.
     * 
     * @param b Feed-forward offset as duty-cycle between -2.0 and 2.0.
     */
    void SetB(double b);


    /**
     * Set PID Proportional gain.
     * 
     * @param kP Proportional gain as a ratio between 0.0 and 4.0.
     */
    void SetKP(double kP);


    /**
     * Set PID Integral gain.
     * 
     * @param kI Integral gain as a ratio between 0.0 and 4.0.
     */
    void SetKI(double kI);


    /**
     * Set PID Derivative gain.
     * 
     * @param kD Derivative gain as a ratio between 0.0 and 4.0.
     */
    void SetKD(double kD);


    /**
     * Set the minimum duty cycle that may be commanded by the PID in
     * SpeedControl, PositionControl, CurrentCurrent and MotionProfile
     * control modes.
     *  
     * @param limit Minimum PID output duty-cycle as a ratio between -1.0 and 1.0.
     */
    void SetMinPILimit(double limit);


    /**
     * Set the maximum duty cycle that may be commanded by the PID in
     * SpeedControl, PositionControl, CurrentCurrent and MotionProfile
     * control modes.
     *  
     * @param limit Maximum PID output duty-cycle as a ratio between -1.0 and 1.0.
     */
    void SetMaxPILimit(double limit);


    /**
     * Set the maximum speed (absolute value of velocity) that may be commanded
     * in the SpeedControl and PositionControl control modes.
     *  
     * @param limit Maximum speed command between 0 and 6000 RPM.
     */
    void SetMaxSpeed(double limit);


    /**
     * Set the maximum acceleration in the SpeedControl and PositionControl
     * control modes.  
     * 
     * <p>This number is used as part of the s-curve path planning
     * in SpeedControl mode and the trapezoid planning in Position Control
     * mode.
     * 
     * <p>Trajectory planning is disabled if the maximum acceleration is zero
     *  
     * @param limit Maximum acceleration between 0 and 25,500 RPM per second 
     */
    void SetMaxAcceleration(double limit);


    /**
     * Set the maximum jerk (second derivitive of speed) in the SpeedControl
     * control mode.  
     * 
     * <p>This number is used as part of the s-curve path planning.
     * 
     * <p>The jerk limit is disabled if the maximum jerk is 0
     *  
     * @param limit Maximum jerk between 0 and 159,375 RPM per second squared.
     */
    void SetMaxJerk(double limit);


    /**
     * Set the Venom motor control mode.
     * 
     * <p>Set the control mode without modifying the motor command. 
     * 
     * <p>The prefered method to change the motor control mode is the 
     * {@link #setCommand} function.  Using setCommand() guarentees the 
     * control mode and the motor command will be received by the Venom
     * controller at the same time.
     * 
     * @param controlMode The commanded control mode.
     */
    void SetControlMode(ControlMode controlMode);


    /**
     * Set the brake/coast behavior when zero is commanded in Proportional
     * and VoltageControl control modes.
     * 
     * @param brakeCoastMode The Brake or Coast behavior in Proportional and VoltageControl modes.
     */
    void SetBrakeCoastMode(BrakeCoastMode brakeCoastMode);


  private: 
    CANVenom_t     *m_canVenomHandle;
    int m_motorID;
};

}