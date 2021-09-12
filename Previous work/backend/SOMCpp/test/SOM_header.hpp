// Forward declare to prevent access errors

#include <vector>
#include <functional>
#include <memory>
#include <vector>
#include <Eigen/Dense>

#define private public
#define protected public

#include <Map2d.hpp>
#include <MapRect.hpp>
#include <MapHex.hpp>
#include <SOM.hpp>
#include <Node.hpp>
#include <LVQ.hpp>
#include <DeepSOM.hpp>

#undef private
#undef protected

template <typename Base, typename T>
inline bool instanceof (const T& v) {
    // const T* ?
    return is_base_of<Base, T>::value;
}

const double EPSILON = 10e-8;