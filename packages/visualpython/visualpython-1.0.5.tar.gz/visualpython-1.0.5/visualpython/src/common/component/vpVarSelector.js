define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpCommon'
], function(requirejs, $, vpConst, sb, vpCommon) {

    const VP_VS_BOX = 'vp-vs-box';
    const VP_VS_DATA_TYPE = 'vp-vs-data-type';
  
    /**
     * @class VarSelector
     * @param {object} pageThis
     * @param {Array} dataTypes
     * @param {String} defaultType
     * @constructor
     */
    var VarSelector = function(pageThis, dataTypes, defaultType='') {
        this.pageThis = pageThis;
        this.dataTypes = dataTypes;
        this.defaultType = defaultType;

        this.attributes = {
            class: []
        }
    }

    VarSelector.setComponentId = function(id) {
        this.attributes.id = id;
    }

    VarSelector.addClass = function(classname) {
        this.attributes.class.push(classname);
    }

    VarSelector.render = function() {
        var tag = new sb.StringBuilder();

        // var selector box
        tag.appendFormatLine('<div class="{0} {1} {2}">', VP_VS_BOX, this.uuid, this.attributes.class.join(' '));

        // hidden input value
        tag.appendFormatLine('<input type="hidden" {0} />', 
                            this.attributes.id? this.attributes.id: '');

        // data type selector
        tag.appendFormatLine('<select class="{0}">', VP_VS_DATA_TYPE);

        tag.appendLine('</select>'); // VP_VS_DATA_TYPE


        tag.appendLine('</div>'); // VP_VS_BOX
    }

    VarSelector.reload = function() {
        // TODO: load using kernel : kernelApi.js
    }

    return VarSelector;
})