#define eigen_assert(x)                                       \
    if (!(x)) {                                               \
        throw(std::runtime_error( "Invalid Eigen operation" )); \
    }  // Throw error instead of aborting straight away when performing invalid Eigen operations
