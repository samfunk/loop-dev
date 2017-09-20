// IMPORTS
import gulp from 'gulp';
import jshint from 'gulp-jshint';
import jscs from 'gulp-jscs';
import nodemon from 'gulp-nodemon';
import babel from 'gulp-babel';
import print from 'gulp-print';
import browserify from 'browserify';
import reactify from 'reactify';
import source from 'vinyl-source-stream';
import clean from 'gulp-clean';

// FILE LISTS
const jsFiles = ['./templates/build/*.js'];
const jsxFiles = ['./src/apps/*.jsx', './src/apps/**/*.jsx'];
const viewFiles = ['./src/views/*.css', './src/views/*.html']
const watchFiles = [jsxFiles, viewFiles];
const buildFolder = './templates/build';
const sourceFile = ['./templates/index.js'];

// CONFIGS
const nodemonOptions = {
    script: './build/srcServer.js',
    delayTime: 1,
    env: {
        'PORT': 8080
    },
    watch: watchFiles
};

// GULP FUNCTIONS
const gulpWatch = function() {
    gulp.watch(watchFiles, function() {
        gulp.run('serve')
    })
}

const gulpClean = function () {
    return gulp.src(buildFolder, {read: false})
        .pipe(clean());
}

const gulpBabelJsx = function() {
    return gulp.src(jsxFiles)
        .pipe(babel({
            plugins: ['transform-react-jsx']
        }))
        .pipe(gulp.dest(buildFolder));
};

const gulpBabelJs = function() {
    return gulp.src(jsFiles)
        .pipe(print())
        .pipe(babel({ presets: ['es2015'] }))
        .pipe(gulp.dest(buildFolder));
};

const gulpBundle = function() {
    return browserify({
        entries: sourceFile,
        debug: true,
    })
    .transform(reactify)
    .bundle()
    .pipe(source('bundle.js'))
    .pipe(gulp.dest(buildFolder));
};

const gulpCopy = function() {
    gulp.src(viewFiles)
    .pipe(gulp.dest(buildFolder));
};

// GULP TASKS
gulp.task('watch', gulpWatch);
gulp.task('clean', gulpClean);
gulp.task('babel-jsx', ['clean'], gulpBabelJsx);
gulp.task('babel', ['babel-jsx'], gulpBabelJs);
gulp.task('bundle', ['babel'], gulpBundle);
gulp.task('build', ['bundle'], gulpCopy);
