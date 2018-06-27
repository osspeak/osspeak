module.exports = {
    target: 'electron-main',
    entry: {
        app: "./src/index.tsx",
        preload: "./src/preload.ts"
    },
    mode: 'development',
    output: {
        filename: "bundle.[name].js",
        path: __dirname + "/dist"
    },

    // Enable sourcemaps for debugging webpack's output.
    devtool: "source-map",

    resolve: {
        // Add '.ts' and '.tsx' as resolvable extensions.
        extensions: [".ts", ".tsx", ".js", ".json"]
    },

    module: {
        rules: [
            {
                test: /\.css$/,
                use: [ 'style-loader', 'css-loader' ]
              },
            // All files with a '.ts' or '.tsx' extension will be handled by 'awesome-typescript-loader'.
            { test: /\.tsx?$/, loader: "awesome-typescript-loader" },
            
        ]
    },
    // externals: {
    //     "react": "React",
    //     "react-dom": "ReactDOM"
    // },
};