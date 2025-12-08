const mix = require("laravel-mix");
const path = require("path")

mix.webpackConfig({
    module: {
        rules: [
            {
                test: /\.pug$/,
                oneOf: [
                    {
                        resourceQuery: /^\?vue/,
                        use: ['pug-plain-loader']
                    },
                    {
                        use: ['raw-loader', 'pug-plain-loader']
                    }
                ]
            },
            {
                test: /\.(png|jpg|jpeg|gif|svg)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[folder]/[name].[ext]',
                            outputPath: 'images/',
                            emitFile: true,
                        }
                    }
                ]
            },
            {
                test: /\.(mp3)$/i,
                loader: 'file-loader',
                exclude: '/public/',
                options: {
                    name: '[name].[ext]',
                    outputPath: 'trash/',
                    emitFile: true,
                },
            },
        ],
    },
    output: {
        chunkFilename: "[name].[chunkhash:8].js",
        filename: "[name].js",
    },
    stats: {
        children: true,
    },
});

mix.alias({
    '@': path.join(__dirname, 'resources/frontend'),
});

mix.copy("resources/frontend/images/**/*", "public/images/")
    .js("resources/frontend/main.js", "public/js")
    .vue()
    .postCss("resources/css/app.css", "public/css", [
        require('postcss-import'),
        require('tailwindcss')("tailwind.config.js"),
        require("autoprefixer")

        // tailwindcss('tailwind.config.js')
    ])
    .extract();
