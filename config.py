# encoding: utf-8

# with out save http response content to database
save_content = False

# http map filenames to MIME types
# https://docs.python.org/2/library/mimetypes.html
http_mimes = ['text', 'image', 'application', 'video', 'message', 'audio']

# http static resource file extension
static_ext = ['js', 'css', 'ico']

# media resource files type
media_types = ['image', 'video', 'audio']

# http static resource files
static_files = [
    'text/css',
    # 'application/javascript',
    # 'application/x-javascript',
    'application/msword',
    'application/vnd.ms-excel',
    'application/vnd.ms-powerpoint',
    'application/x-ms-wmd',
    'application/x-shockwave-flash',
    # 'image/x-cmu-raster',
    # 'image/x-ms-bmp',
    # 'image/x-portable-graymap',
    # 'image/x-portable-bitmap',
    # 'image/jpeg',
    # 'image/gif',
    # 'image/x-xwindowdump',
    # 'image/png',
    # 'image/vnd.microsoft.icon',
    # 'image/x-portable-pixmap',
    # 'image/x-xpixmap',
    # 'image/ief',
    # 'image/x-portable-anymap',
    # 'image/x-rgb',
    # 'image/x-xbitmap',
    # 'image/tiff',
    # 'video/mpeg',
    # 'video/x-sgi-movie',
    # 'video/mp4',
    # 'video/x-msvideo',
    # 'video/quicktime'
    # 'audio/mpeg',
    # 'audio/x-wav',
    # 'audio/x-aiff',
    # 'audio/basic',
    # 'audio/x-pn-realaudio',
]

# 打卡地址信息分别是地址信息的unicode编码, longitude经度, latitude纬度
address_info = [u'\u65b9\u821f\u5927\u53a6', '121.4815163612', '31.2649791194']
