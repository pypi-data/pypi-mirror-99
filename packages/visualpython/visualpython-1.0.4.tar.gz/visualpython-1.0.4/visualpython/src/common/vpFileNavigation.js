define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpCommon'
], function(requirejs, $, vpConst, sb, vpCommon) {
    
    // Temporary constant data


    /**
     * @class FileNavigation
     * @param {string} type
     * @param {object} state
     * @constructor
     */
    var FileNavigation = function(type, state) {
        this.uuid = vpCommon.getUUID();
        this.type = type;
        this.state = { ...state };

        this.init();
    }

    /**
     * File Types
     */
    FileNavigation.FILE_TYPE = {
        SAVE_VP_NOTE: 'save_vp_note',
        OPEN_VP_NOTE: 'open_vp_note',
        SAVE_FILE: 'save_file',
        OPEN_FILE: 'open_file',
        SAVE_IMG_FILE: 'save_img_file',
        OPEN_IMG_FILE: 'open_img_file'
    }

    FileNavigation.prototype.init = async function() {
        var that = this;

        var loadURLstyle = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH;
        var loadURLhtml = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.SOURCE_PATH + "component/fileNavigation/index.html";
        
        vpCommon.loadCss( loadURLstyle + "component/fileNavigation.css");

        await $(`<div id="vp_fileNavigation"></div>`).load(loadURLhtml, () => {           
            that.renderThis();
            that.bindEvent();

            that.open();
        }).appendTo("#site");
    }

    FileNavigation.prototype.open = function() {
        $('#vp_fileNavigation').show();
    }

    FileNavigation.prototype.close = function() {
        $('#vp_fileNavigation').hide();
    }

    FileNavigation.prototype.renderThis = function() {

    }

    FileNavigation.prototype.bindEvent = function() {

    }

    return FileNavigation;
});