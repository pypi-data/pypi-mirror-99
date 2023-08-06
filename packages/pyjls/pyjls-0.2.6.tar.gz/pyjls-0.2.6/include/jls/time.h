/*
 * Copyright 2014-2021 Jetperch LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @file
 *
 * @brief JLS time representation.
 */

#ifndef JLS_TIME_H__
#define JLS_TIME_H__

#include "jls/cmacro.h"
#include <stdint.h>

/**
 * @ingroup jls
 * @defgroup jls_time Time representation
 *
 * @brief JLS time representation.
 *
 * The C standard library includes time.h which is very inconvenient for any
 * precision application.  This module defines a much simpler 64-bit fixed point
 * integer for representing time.  The value is 34Q30 with the upper 34 bits
 * to represent whole seconds and the lower 30 bits to represent fractional
 * seconds.  A value of 2**30 (1 << 30) represents 1 second.  This
 * representation gives a resolution of 2 ** -30 (approximately 1 nanosecond)
 * and a range of +/- 2 ** 33 (approximately 272 years).  The value is
 * signed to allow for simple arithmetic on the time either as a fixed value
 * or as deltas.
 *
 * Certain elements may elect to use floating point time given in seconds.
 * The macros JLS_TIME_TO_F64() and JLS_F64_TO_TIME() facilitate
 * converting between the domains.  Note that double precision floating
 * point is not able to maintain the same resolution over the time range
 * as the 64-bit representation.  JLS_TIME_TO_F32() and JLS_F32_TO_TIME()
 * allow conversion to single precision floating point which has significantly
 * reduce resolution compared to the 34Q30 value.
 *
 * @{
 */

JLS_CPP_GUARD_START

/**
 * @brief The number of fractional bits in the 64-bit time representation.
 */
#define JLS_TIME_Q 30

/**
 * @brief The maximum (positive) time representation
 */
#define JLS_TIME_MAX ((int64_t) 0x7fffffffffffffffU)

/**
 * @brief The minimum (negative) time representation.
 */
#define JLS_TIME_MIN ((int64_t) 0x8000000000000000U)

/**
 * @brief The offset from the standard UNIX (POSIX) epoch.
 *
 * This offset allows translation between jls time and the 
 * standard UNIX (POSIX) epoch of Jan 1, 1970.
 *
 * The value was computed using python3:
 *
 *     import dateutil.parser
 *     dateutil.parser.parse('2018-01-01T00:00:00Z').timestamp()
 *
 * JLS chooses a different epoch to advance "zero" by 48 years!
 */
#define JLS_TIME_EPOCH_UNIX_OFFSET_SECONDS 1514764800

/**
 * @brief The fixed-point representation for 1 second.
 */
#define JLS_TIME_SECOND (((int64_t) 1) << JLS_TIME_Q)

/// The mask for the fractional bits
#define JLS_FRACT_MASK (JLS_TIME_SECOND - 1)

/**
 * @brief The approximate fixed-point representation for 1 millisecond.
 */
#define JLS_TIME_MILLISECOND ((JLS_TIME_SECOND + 500) / 1000)

/**
 * @brief The approximate fixed-point representation for 1 microsecond.
 *
 * CAUTION: this value is 0.024% accurate (240 ppm)
 */
#define JLS_TIME_MICROSECOND ((JLS_TIME_SECOND + 500000) / 1000000)

/**
 * @brief The approximate fixed-point representation for 1 nanosecond.
 *
 * WARNING: this value is only 6.7% accurate!
 */
#define JLS_TIME_NANOSECOND ((int64_t) 1)

/**
 * @brief The fixed-point representation for 1 minute.
 */
#define JLS_TIME_MINUTE (JLS_TIME_SECOND * 60)

/**
 * @brief The fixed-point representation for 1 hour.
 */
#define JLS_TIME_HOUR (JLS_TIME_MINUTE * 60)

/**
 * @brief The fixed-point representation for 1 day.
 */
#define JLS_TIME_DAY (JLS_TIME_HOUR * 24)

/**
 * @brief The fixed-point representation for 1 week.
 */
#define JLS_TIME_WEEK (JLS_TIME_DAY * 7)

/**
 * @brief The average fixed-point representation for 1 month (365 day year).
 */
#define JLS_TIME_MONTH (JLS_TIME_YEAR / 12)

/**
 * @brief The approximate fixed-point representation for 1 year (365 days).
 */
#define JLS_TIME_YEAR (JLS_TIME_DAY * 365)

/**
 * @brief Convert the 64-bit fixed point time to a double.
 *
 * @param x The 64-bit signed fixed point time.
 * @return The time as a double p.  Note that IEEE 747 doubles only have
 *      52 bits of precision, so the result will be truncated for very
 *      small deltas.
 */
#define JLS_TIME_TO_F64(x) (((double) (x)) / ((double) JLS_TIME_SECOND))

/**
 * @brief Convert the double precision time to 64-bit fixed point time.
 *
 * @param x The double-precision floating point time in seconds.
 * @return The time as a 34Q30.
 */
static inline int64_t JLS_F64_TO_TIME(double x) {
    if (x < 0) {
        return -JLS_F64_TO_TIME(-x);
    }
    return (int64_t) ((x * (double) JLS_TIME_SECOND) + 0.5);
}

/**
 * @brief Convert the 64-bit fixed point time to single precision float.
 *
 * @param x The 64-bit signed fixed point time.
 * @return The time as a float p in seconds.  Note that IEEE 747 singles only
 *      have 23 bits of precision, so the result will likely be truncated.
 */
#define JLS_TIME_TO_F32(x) (((float) (x)) / ((float) JLS_TIME_SECOND))

/**
 * @brief Convert the single precision float time to 64-bit fixed point time.
 *
 * @param x The single-precision floating point time in seconds.
 * @return The time as a 34Q30.
 */
static inline int64_t JLS_F32_TO_TIME(float x) {
    if (x < 0.0f) {
        return -JLS_F32_TO_TIME(-x);
    }
    return (int64_t) ((x * (float) JLS_TIME_SECOND) + 0.5f);
}

/**
 * @brief Convert to counter ticks, rounded to nearest.
 *
 * @param x The 64-bit signed fixed point time.
 * @param z The counter frequency in Hz.
 * @return The 64-bit time in counter ticks.
 */
static inline int64_t JLS_TIME_TO_COUNTER(int64_t x, uint64_t z) {
    if (x < 0) {
        return -JLS_TIME_TO_COUNTER(-x, z);
    }
    // return (int64_t) ((((x * z) >> (JLS_TIME_Q - 1)) + 1) >> 1);
    uint64_t c = (((x & ~JLS_FRACT_MASK) >> (JLS_TIME_Q - 1)) * z);
    uint64_t fract = (x & JLS_FRACT_MASK) << 1;
    c += ((fract * z) >> JLS_TIME_Q) + 1;
    return (int64_t) (c >> 1);
}

/**
 * @brief Convert to counter ticks, rounded towards zero
 *
 * @param x The 64-bit signed fixed point time.
 * @param z The counter frequency in Hz.
 * @return The 64-bit time in counter ticks.
 */
static inline int64_t JLS_TIME_TO_COUNTER_RZERO(int64_t x, uint64_t z) {
    if (x < 0) {
        return -JLS_TIME_TO_COUNTER_RZERO(-x, z);
    }
    uint64_t c = (x >> JLS_TIME_Q) * z;
    c += ((x & JLS_FRACT_MASK) * z) >> JLS_TIME_Q;
    return (int64_t) c;
}

/**
 * @brief Convert to counter ticks, rounded towards infinity.
 *
 * @param x The 64-bit signed fixed point time.
 * @param z The counter frequency in Hz.
 * @return The 64-bit time in counter ticks.
 */
static inline int64_t JLS_TIME_TO_COUNTER_RINF(int64_t x, uint64_t z) {
    if (x < 0) {
        return -JLS_TIME_TO_COUNTER_RINF(-x, z);
    }
    x += JLS_TIME_SECOND - 1;
    uint64_t c = (x >> JLS_TIME_Q) * z;
    c += ((x & JLS_FRACT_MASK) * z) >> JLS_TIME_Q;
    return (int64_t) c;
}

/**
 * @brief Convert to 32-bit unsigned seconds.
 *
 * @param x The 64-bit signed fixed point time.
 * @return The 64-bit unsigned time in seconds, rounded to nearest.
 */
#define JLS_TIME_TO_SECONDS(x) JLS_TIME_TO_COUNTER(x, 1)

/**
 * @brief Convert to milliseconds.
 *
 * @param x The 64-bit signed fixed point time.
 * @return The 64-bit signed time in milliseconds, rounded to nearest.
 */
#define JLS_TIME_TO_MILLISECONDS(x) JLS_TIME_TO_COUNTER(x, 1000)

/**
 * @brief Convert to microseconds.
 *
 * @param x The 64-bit signed fixed point time.
 * @return The 64-bit signed time in microseconds, rounded to nearest.
 */
#define JLS_TIME_TO_MICROSECONDS(x) JLS_TIME_TO_COUNTER(x, 1000000)

/**
 * @brief Convert to nanoseconds.
 *
 * @param x The 64-bit signed fixed point time.
 * @return The 64-bit signed time in nanoseconds, rounded to nearest.
 */
#define JLS_TIME_TO_NANOSECONDS(x) JLS_TIME_TO_COUNTER(x, 1000000000ll)

/**
 * @brief Convert a counter to 64-bit signed fixed point time.
 *
 * @param x The counter value in ticks.
 * @param z The counter frequency in Hz.
 * @return The 64-bit signed fixed point time.
 */
static inline int64_t JLS_COUNTER_TO_TIME(uint64_t x, uint64_t z) {
    // compute (x << JLS_TIME_Q) / z, but without unnecessary saturation
    uint64_t seconds = x / z;
    uint64_t remainder = x - (seconds * z);
    uint64_t fract = (remainder << JLS_TIME_Q) / z;
    uint64_t t = (int64_t) ((seconds << JLS_TIME_Q) + fract);
    return t;
}

/**
 * @brief Convert to 64-bit signed fixed point time.
 *
 * @param x he 32-bit unsigned time in seconds.
 * @return The 64-bit signed fixed point time.
 */
#define JLS_SECONDS_TO_TIME(x) (((int64_t) (x)) << JLS_TIME_Q)

/**
 * @brief Convert to 64-bit signed fixed point time.
 *
 * @param x The 32-bit unsigned time in milliseconds.
 * @return The 64-bit signed fixed point time.
 */
#define JLS_MILLISECONDS_TO_TIME(x) JLS_COUNTER_TO_TIME(x, 1000)

/**
 * @brief Convert to 64-bit signed fixed point time.
 *
 * @param x The 32-bit unsigned time in microseconds.
 * @return The 64-bit signed fixed point time.
 */
#define JLS_MICROSECONDS_TO_TIME(x) JLS_COUNTER_TO_TIME(x, 1000000)

/**
 * @brief Convert to 64-bit signed fixed point time.
 *
 * @param x The 32-bit unsigned time in microseconds.
 * @return The 64-bit signed fixed point time.
 */
#define JLS_NANOSECONDS_TO_TIME(x) JLS_COUNTER_TO_TIME(x, 1000000000ll)

/**
 * @brief Compute the absolute value of a time.
 *
 * @param t The time.
 * @return The absolute value of t.
 */
static inline int64_t JLS_TIME_ABS(int64_t t) {
    return ( (t) < 0 ? -(t) : (t) );
}

/**
 * @brief Get the UTC time as a 34Q30 fixed point number.
 *
 * @return The current time.  This value is not guaranteed to be monotonic.
 *      The device may synchronize to external clocks which can cause
 *      discontinuous jumps, both backwards and forwards.
 *
 *      At power-on, the time will start from 0 unless the system has
 *      a real-time clock.  When the current time first synchronizes to
 *      an external host, it may have a large skip.
 *
 * Be sure to verify your time for each platform using python:
 *
 *      python
 *      import datetime
 *      import dateutil.parser
 *      epoch = dateutil.parser.parse('2018-01-01T00:00:00Z').timestamp()
 *      datetime.datetime.fromtimestamp((my_time >> 30) + epoch)
 */
JLS_API int64_t jls_now();

/**
 * @brief The platform counter structure.
 */
struct jls_time_counter_s {
    /// The counter value.
    uint64_t value;
    /// The approximate counter frequency.
    uint64_t frequency;
};

/**
 * @brief Get the monotonic platform counter.
 *
 * @return The monotonic platform counter.
 *
 * The platform implementation may select an appropriate source and
 * frequency.  The JLS library assumes a nominal frequency of
 * at least 1000 Hz, but we frequencies in the 1 MHz to 100 MHz
 * range to enable profiling.  The frequency should not exceed 10 GHz
 * to prevent rollover.
 *
 * The counter must be monotonic.  If the underlying hardware is less
 * than the full 64 bits, then the platform must unwrap and extend
 * the hardware value to 64-bit.
 *
 * The JLS authors recommend this counter starts at 0 when the
 * system powers up.
 */
JLS_API struct jls_time_counter_s jls_time_counter();

/**
 * @brief Get the monotonic platform time as a 34Q30 fixed point number.
 *
 * @return The monotonic platform time based upon the jls_time_counter().
 *      The platform time has no guaranteed relationship with
 *      UTC or wall-clock calendar time.  This time has both
 *      offset and scale errors relative to UTC.
 */
static inline int64_t jls_time_rel() {
    struct jls_time_counter_s counter = jls_time_counter();
    return JLS_COUNTER_TO_TIME(counter.value, counter.frequency);
}

JLS_CPP_GUARD_END

/** @} */

#endif /* JLS_TIME_H__ */
