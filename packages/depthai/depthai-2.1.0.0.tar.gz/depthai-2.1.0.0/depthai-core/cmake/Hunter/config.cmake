hunter_config(
    nlohmann_json
    VERSION "3.9.1"
    URL "https://github.com/nlohmann/json/archive/v3.9.1.tar.gz"
    SHA1 "f8a20a7e19227906d77de0ede97468fbcfea03e7"
)

hunter_config(
    XLink
    VERSION "luxonis-2021.2-develop"
    URL "https://github.com/luxonis/XLink/archive/ee361ecba950335390ad539e509f8ab96313b6b4.tar.gz"
    SHA1 "72108319bf2289d91157a3933663ed5fb2b6eb18"
)

hunter_config(
    BZip2
    VERSION "1.0.8-p0"
)

hunter_config(
    spdlog
    VERSION "1.8.2"
    URL "https://github.com/gabime/spdlog/archive/v1.8.2.tar.gz"
    SHA1 "4437f350ca7fa89a0cd8faca1198afb36823f775"
    CMAKE_ARGS
        SPDLOG_BUILD_EXAMPLE=OFF
        SPDLOG_FMT_EXTERNAL=OFF
)

# libarchive, luxonis fork
hunter_config(
    libarchive
    VERSION "3.4.2-p2"
    URL "https://github.com/luxonis/libarchive/archive/cf2caf0588fc5e2af22cae37027d3ff6902e096f.tar.gz"
    SHA1 "e99477d32ce14292fe652dc5f4f460d3af8fbc93"
    CMAKE_ARGS
        ENABLE_ACL=OFF                                           
        ENABLE_BZip2=OFF                                          
        ENABLE_CAT=OFF                                          
        ENABLE_CAT_SHARED=OFF                                          
        ENABLE_CNG=OFF                                          
        ENABLE_COVERAGE=OFF                                          
        ENABLE_CPIO=OFF                                          
        ENABLE_CPIO_SHARED=OFF                                          
        ENABLE_EXPAT=OFF                                          
        ENABLE_ICONV=OFF                                          
        ENABLE_INSTALL=ON                                          
        ENABLE_LIBB2=OFF                                          
        ENABLE_LIBXML2=OFF                                          
        ENABLE_LZ4=OFF                                          
        ENABLE_LZMA=ON                                           
        ENABLE_LZO=OFF                                          
        ENABLE_LibGCC=OFF                                          
        ENABLE_MBEDTLS=OFF                                          
        ENABLE_NETTLE=OFF                                          
        ENABLE_OPENSSL=OFF                                          
        ENABLE_PCREPOSIX=OFF                                          
        ENABLE_SAFESEH=AUTO                                         
        ENABLE_TAR=OFF                                           
        ENABLE_TAR_SHARED=OFF                                          
        ENABLE_TEST=OFF                                          
        ENABLE_WERROR=OFF                                           
        ENABLE_XATTR=OFF                                          
        ENABLE_ZLIB=OFF                                          
        ENABLE_ZSTD=OFF
)
