<!DOCTYPE html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" type="image/png" href="{{ asset('/images/favicon.png') }}">

        <title>Laravel</title>

        <!-- Fonts -->
        <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&family=Rubik:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="{{ asset('/css/app.css') }}?v={{time()}}">
    </head>
    <body 
    class="
      [&_b]:font-bold
      [&_span]:cursor-default [&_p]:cursor-default [&_h1]:cursor-default [&_h2]:cursor-default [&_h3]:cursor-default [&_h4]:cursor-default 
      [&_h5]:cursor-default [&_h6]:cursor-default 
      [&_img]:pointer-events-none
      [&_li]:list-none
      bg-[#1b1c20]
      font-['Manrope']
      text-white
      [&_div.vm--overlay]:bg-[#1b1c20]/[0.8]
      [&_div.vm--modal]:bg-[#303038]
      [&_div.vm--modal]:rounded-xl
      [&_div.vm--modal]:shadow-none
      [&_div.toast-top-center]:top-[16px]
      [&_div.toast-container>div]:shadow-none
      [&_div.toast-success]:bg-violet
      hover:[&_div.toast-success]:bg-violetHover
      [&_div.toast-error]:bg-red
      hover:[&_div.toast-error]:bg-redHover
      [&_div.toast-container>div]:bg-[length:16px_16px]
      [&_div.toast-container>div]:pr-[20px]
      [&_div.toast-container>div]:pt-[12px]
      [&_div.toast-container>div]:pb-[15px]
      [&_div.toast-container>div]:text-sm
      [&_div.toast-container>div]:opacity-100
      [&_div.toast-container>div]:rounded-xl
      [&_div.toast-container>div]:pl-[45px]
      [&_div.toast]:transition-all
      [&_div.toast]:duration-200
    "
  >
        <div id="app"></div>
    </body>
    <script src="{{ asset('/js/manifest.js') }}?v={{time()}}"></script>
    <script src="{{ asset('/js/vendor.js') }}?v={{time()}}"></script>
    <script src="{{ asset('/js/main.js') }}?v={{time()}}"></script>
</html>
