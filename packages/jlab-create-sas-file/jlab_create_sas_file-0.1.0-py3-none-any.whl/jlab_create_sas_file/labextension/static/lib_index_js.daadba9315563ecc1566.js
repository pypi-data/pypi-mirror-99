(self["webpackChunkjlab_create_sas_file"] = self["webpackChunkjlab_create_sas_file"] || []).push([["lib_index_js"],{

/***/ "./lib/iconImport.js":
/*!***************************!*\
  !*** ./lib/iconImport.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "sasIcon": () => /* binding */ sasIcon
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_sas_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/icons/sas.svg */ "./style/icons/sas.svg");


const sasIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'jlab_create_sas_file:sas2',
    svgstr: _style_icons_sas_svg__WEBPACK_IMPORTED_MODULE_1__.default
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => __WEBPACK_DEFAULT_EXPORT__
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _iconImport__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./iconImport */ "./lib/iconImport.js");





const FACTORY = 'Editor';
const PALETTE_CATEGORY = 'Text Editor';
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.createNew = 'fileeditor:create-new-sas-file';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the jlab-create-sas-file extension.
 */
const extension = {
    id: 'jlab-create-sas-file:plugin',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__.IFileBrowserFactory],
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__.ILauncher, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    activate: (app, browserFactory, launcher, menu, palette) => {
        const { commands } = app;
        const command = CommandIDs.createNew;
        commands.addCommand(command, {
            label: args => (args['isPalette'] ? 'New SAS File' : 'SAS File'),
            caption: 'Create a new SAS file',
            icon: _iconImport__WEBPACK_IMPORTED_MODULE_4__.sasIcon,
            execute: async (args) => {
                const cwd = args['cwd'] || browserFactory.defaultBrowser.model.path;
                const model = await commands.execute('docmanager:new-untitled', {
                    path: cwd,
                    type: 'file',
                    ext: 'sas'
                });
                return commands.execute('docmanager:open', {
                    path: model.path,
                    factory: FACTORY
                });
            }
        });
        // add to the launcher
        if (launcher) {
            launcher.add({
                command,
                category: 'Other',
                rank: 1
            });
        }
        // add to the palette
        if (palette) {
            palette.addItem({
                command,
                args: { isPalette: true },
                category: PALETTE_CATEGORY
            });
        }
        // add to the menu
        if (menu) {
            menu.fileMenu.newMenu.addGroup([{ command }], 30);
        }
        // add to context menu
        app.contextMenu.addItem({
            command: command,
            selector: '.jp-DirListing-content',
            rank: 0
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./style/icons/sas.svg":
/*!*****************************!*\
  !*** ./style/icons/sas.svg ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => __WEBPACK_DEFAULT_EXPORT__
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<!-- Generator: Adobe Illustrator 24.0.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->\n<svg version=\"1.1\" id=\"Layer_1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\"\n\t viewBox=\"0 0 48 48\" style=\"enable-background:new 0 0 48 48;\" xml:space=\"preserve\">\n<style type=\"text/css\">\n\t.st0{fill:#007DC3;}\n\t.st1{fill:#FFFFFF;}\n</style>\n<rect class=\"st0\" width=\"47.7\" height=\"47.7\"/>\n<g>\n\t<g>\n\t\t<g>\n\t\t\t<g>\n\t\t\t\t<path class=\"st1\" d=\"M27,16.4l-0.7-0.8c-0.9-1.1-2.4-1.1-3.5-0.2s-1.4,2.4-0.5,3.5c0,0,0.1,0.1,0.3,0.4\"/>\n\t\t\t\t<path class=\"st1\" d=\"M22.7,19.3c2.1,2.5,4.8,5.8,4.8,5.8c3.5,4.2,1.9,9.4-2.8,12.3C20.6,40,13,39.1,10.4,34.8\n\t\t\t\t\tc2,6,8.8,9.9,16.4,8c6.5-1.6,13.8-10,5.8-19.7L26.7,16\"/>\n\t\t\t</g>\n\t\t\t<path class=\"st1\" d=\"M23.3,28.3c-2-2.4-4.5-5.4-4.5-5.4c-3.5-4.2-1.9-9.4,2.8-12.3C25.8,8,33.4,8.9,36,13.2c-2-6-8.8-9.9-16.4-8\n\t\t\t\tc-6.5,1.6-13.8,10-5.8,19.7l5.7,6.8\"/>\n\t\t\t<path class=\"st1\" d=\"M18.5,30.6l1.3,1.6c0.9,1.1,2.4,1.1,3.5,0.2s1.4-2.4,0.5-3.5c0,0-0.5-0.6-1.3-1.6\"/>\n\t\t</g>\n\t</g>\n\t<g>\n\t\t<path class=\"st1\" d=\"M37,34.9c0-0.7,0.5-1.2,1.2-1.2c0.7,0,1.2,0.5,1.2,1.2c0,0.7-0.5,1.3-1.2,1.3C37.5,36.2,37,35.6,37,34.9z\n\t\t\t M38.2,36.4c0.8,0,1.5-0.6,1.5-1.5c0-0.9-0.7-1.5-1.5-1.5c-0.8,0-1.5,0.6-1.5,1.5C36.6,35.8,37.4,36.4,38.2,36.4z M37.9,35h0.3\n\t\t\tl0.5,0.8h0.3L38.4,35c0.3,0,0.4-0.2,0.4-0.5c0-0.3-0.2-0.5-0.6-0.5h-0.7v1.7h0.3C37.9,35.8,37.9,35,37.9,35z M37.9,34.8v-0.5h0.4\n\t\t\tc0.2,0,0.4,0,0.4,0.3c0,0.3-0.2,0.3-0.4,0.3L37.9,34.8L37.9,34.8z\"/>\n\t</g>\n</g>\n</svg>\n");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.daadba9315563ecc1566.js.map