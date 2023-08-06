const { param } = require("jquery");

define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/component/vpSuggestInputText'
], function(requirejs, $, vpConst, sb, vpCommon, vpSuggestInputText) {


    // temporary const
    const VP_DIR_BOX = 'vp-dir-box';
    const VP_DIR_SELECT_CONTAINER = 'vp-dir-select-container';
    const VP_DIR_SELECT_TITLE = 'vp-dir-select-title';
    const VP_DIR_SEARCH = 'vp-dir-search';
    const VP_DIR_TYPE = 'vp-dir-type';
    const VP_DIR_SELECT_BOX = 'vp-dir-select-box';
    const VP_DIR_SELECT_LIST = 'vp-dir-select-list';
    const VP_DIR_SELECT_ITEM = 'vp-dir-select-item';

    const VP_DIR_PARAMETER_BOX = 'vp-dir-parameter-box';
    const VP_DIR_PARAMETER = 'vp-dir-parameter';

    // function/method types
    var _METHOD_TYPES = ['function', 'method', 'type', 'builtin_function_or_method', 'PlotAccessor'];

    /**
     * @class DirBox
     * @param {object} pageThis
     * @param {string} targetId
     * @param {boolean} popup
     * @constructor
     */
    var DirBox = function(pageThis, targetId, containerId='vp-wrapper', popup=false) {
        this.pageThis = pageThis;
        this.targetId = targetId;
        this.uuid = vpCommon.getUUID();
        this.containerId = containerId;
        this.popup = popup;

        this.state = {
            code: '',
            type: '',
            list: []
        }

        this.bindEvent();
        this.init();
        
    }

    DirBox.prototype.getVarType = function() {
        return this.state.type;
    }

    DirBox.prototype.getVarList = function() {
        return this.state.list;
    }

    DirBox.prototype.init = function() {
        // load css
        this.pageThis.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "common/dirBox.css");

        this.renderThis();
        this.reload();
    }
    
    DirBox.prototype.wrapSelector = function(selector='') {
        return vpCommon.formatString('.{0} {1}', this.uuid, selector);
    }

    DirBox.prototype.renderThis = function(replace=true) {
        var tag = new sb.StringBuilder();
        tag.appendFormatLine('<div class="{0} {1}">', VP_DIR_BOX, this.uuid); // vp-select-base

        tag.appendFormatLine('<div class="{0} {1}">', VP_DIR_SELECT_CONTAINER, 'attr');
        tag.appendFormatLine('<div class="vp-multilang {0}">Attribute</div>', VP_DIR_SELECT_TITLE);
        tag.appendFormatLine('<input class="vp-input {0} {1}" type="text" placeholder="search attribute" />', VP_DIR_SEARCH, 'attr');
        tag.appendFormatLine('<input class="{0} {1}" type="hidden"/>', VP_DIR_TYPE, 'attr');
        tag.appendFormatLine('<div class="{0} {1}">', VP_DIR_SELECT_BOX, 'attr');
        tag.appendFormatLine('<ul class="{0} {1}">', VP_DIR_SELECT_LIST, 'attr');
        tag.appendLine('</ul>');
        tag.appendLine('</div>'); // VP_DIR_SELECT_BOX
        tag.appendLine('</div>'); // VP_DIR_SELECT_CONTAINER

        tag.appendFormatLine('<div class="{0} {1}">', VP_DIR_SELECT_CONTAINER, 'method');
        tag.appendFormatLine('<div class="vp-multilang {0}">Method</div>', VP_DIR_SELECT_TITLE);
        tag.appendFormatLine('<input class="vp-input {0} {1}" type="text" placeholder="search method" />', VP_DIR_SEARCH, 'method');
        tag.appendFormatLine('<input class="{0} {1}" type="hidden"/>', VP_DIR_TYPE, 'method');
        tag.appendFormatLine('<div class="{0} {1}">', VP_DIR_SELECT_BOX, 'method');
        tag.appendFormatLine('<ul class="{0} {1}">', VP_DIR_SELECT_LIST, 'method');
        tag.appendLine('</ul>');
        tag.appendLine('</div>'); // VP_DIR_SELECT_BOX
        tag.appendLine('</div>'); // VP_DIR_SELECT_CONTAINER

        tag.appendFormatLine('<div class="{0}">', VP_DIR_PARAMETER_BOX);
        tag.appendFormatLine('<input type="text" class="{0}" placeholder="{1}"/>'
                            , VP_DIR_PARAMETER, 'input parameter');
        tag.appendLine('</div>'); // VP_DIR_PARAMETER

        tag.appendLine('</div>'); // VP_DIR_BOX END

        // TODO: if this.popup == true

        $(this.pageThis.wrapSelector('#' + this.containerId)).html(tag.toString());

        return tag.toString();
    }

    DirBox.prototype.bindEvent = function() {
        var that = this;
        // select attribute
        $(document).on('click', this.wrapSelector('.' + VP_DIR_SELECT_LIST + '.attr .' + VP_DIR_SELECT_ITEM), function(event) {
            var varName = $(this).attr('data-var-name');
            var varType = $(this).attr('data-var-type');

            console.log('clicked', varName, varType);
            $(that.pageThis.wrapSelector('#' + that.targetId)).trigger({
                type:"dirbox_selected",
                varName: varName,
                varType: varType,
                isMethod: false
            });
        });

        // select method
        $(document).on('click', this.wrapSelector('.' + VP_DIR_SELECT_LIST + '.method .' + VP_DIR_SELECT_ITEM), function(event) {
            var varName = $(this).attr('data-var-name');
            var varType = $(this).attr('data-var-type');
            console.log('clicked', varName, varType);
            $(that.pageThis.wrapSelector('#' + that.targetId)).trigger({
                type:"dirbox_selected",
                varName: varName,
                varType: varType,
                isMethod: true
            });
        });

        // parameter input
        $(document).on('change', this.wrapSelector('.' + VP_DIR_PARAMETER), function(event) {
            var parameter = $(this).val();
            var variable = $(that.pageThis.wrapSelector('#' + that.targetId)).val();
            var splitList = variable.split('.');
            if (splitList && splitList.length > 0) {
                var lastSplit = splitList[splitList.length - 1];
                var matchList = lastSplit.match(/\(.*?\)$/gi);
                if (matchList && matchList.length > 0) {
                    var lastBracket = matchList[matchList.length - 1];
                    splitList[splitList.length - 1] = lastSplit.replace(lastBracket, vpCommon.formatString('({0})', parameter));
                    var newCode = splitList.join('.');
                    $(that.pageThis.wrapSelector('#' + that.targetId)).trigger({
                        type:"dirbox_replace",
                        originCode: variable,
                        newCode: newCode
                    });
                }
            }
                
        });
    }

    DirBox.prototype.reload = function(callback=undefined) {
        var that = this;
        var variable = $(this.pageThis.wrapSelector('#' + this.targetId)).val();
        this.state.code = variable;
        
        var code = vpCommon.formatString('_vp_print(_vp_load_instance("{0}"))', variable);

        this.pageThis.kernelExecute(code, function(result) {
            var varObj = {
                type: 'None',
                list: []
            };
            try {
                varObj = JSON.parse(result);
            } catch {
                ; // command error
            }

            var varType = varObj.type;
            var varList = varObj.list;

            that.state.type = varType;
            that.state.list = varList;

            // set variable type
            // $(that.wrapSelector('#vp_instanceType')).text(varType);

            // set dir list
            var attrListTag = new sb.StringBuilder();
            var methodListTag = new sb.StringBuilder();
            var attrList = [];
            var methodList = [];
            varList != undefined && varList.forEach(obj => {
                if (obj.type.includes('Indexer')) {
                    methodListTag.appendFormatLine('<li class="{0}" data-var-name="{1}" data-var-type="{2}"><span>{3}</span>{4}</li>'
                                                , VP_DIR_SELECT_ITEM, obj.name + '[]', obj.type, obj.type, obj.name);
                    methodList.push({
                        label: obj.name + '[]' + ' (' + obj.type + ')',
                        value: obj.name + '[]',
                        type: obj.type 
                    });
                }
                // Method/Function... 이면 Method 항목에 표시
                else if (_METHOD_TYPES.includes(obj.type)) {
                    methodListTag.appendFormatLine('<li class="{0}" data-var-name="{1}" data-var-type="{2}"><span>{3}</span>{4}</li>'
                                                , VP_DIR_SELECT_ITEM, obj.name + '()', obj.type, obj.type, obj.name);
                    methodList.push({
                        label: obj.name + '()' + ' (' + obj.type + ')',
                        value: obj.name + '()' ,
                        type: obj.type
                    });
                } else {
                    // FIXME: type이 module일 경우엔 pd(pandas) module만 표시
                    // if (obj.type == 'module' && obj.name != 'pd') {
                    //     ;
                    // } else {
                    attrListTag.appendFormatLine('<li class="{0}" data-var-name="{1}" data-var-type="{2}"><span>{3}</span>{4}</li>'
                                                , VP_DIR_SELECT_ITEM, obj.name, obj.type, obj.type, obj.name);
                    attrList.push({
                        label: obj.name + ' (' + obj.type + ')',
                        value: obj.name,
                        type: obj.type
                    });
                    // }
                }
            });
            $(that.wrapSelector('.' + VP_DIR_SELECT_LIST + '.attr')).html(attrListTag.toString());
            $(that.wrapSelector('.' + VP_DIR_SELECT_LIST + '.method')).html(methodListTag.toString());

            // attribute search suggest
            var suggestInput = new vpSuggestInputText.vpSuggestInputText();
            suggestInput.addClass('vp-input attr');
            suggestInput.addClass(VP_DIR_SEARCH);
            suggestInput.setPlaceholder("search attribute");
            suggestInput.setSuggestList(function() { return attrList; });
            suggestInput.setSelectEvent(function(value, item) {
                $(this.wrapSelector()).val(value);
                $(that.wrapSelector('.' + VP_DIR_TYPE + '.attr')).val(item.type);
            });
            $(that.wrapSelector('.' + VP_DIR_SEARCH + '.attr')).replaceWith(function() {
                return suggestInput.toTagString();
            });

            // method search suggest
            suggestInput = new vpSuggestInputText.vpSuggestInputText();
            suggestInput.addClass('vp-input method');
            suggestInput.addClass(VP_DIR_SEARCH);
            suggestInput.setPlaceholder("search method");
            suggestInput.setSuggestList(function() { return methodList; });
            suggestInput.setSelectEvent(function(value, item) {
                $(this.wrapSelector()).val(value);
                $(that.wrapSelector('.' + VP_DIR_TYPE + '.method')).val(item.type);
            });
            $(that.wrapSelector('.' + VP_DIR_SEARCH + '.method')).replaceWith(function() {
                return suggestInput.toTagString();
            });

            // get parameter
            var splitList = variable.split('.');
            if (splitList && splitList.length > 0) {
                var lastSplit = splitList[splitList.length - 1];
                // if bracket is at the end of code
                var matchList = lastSplit.match(/\(.*?\)$/gi);
                if (matchList != null && matchList.length > 0) {
                    var lastBracket = matchList[matchList.length - 1];
                    // remove first/last brackets
                    var parameter = lastBracket.substr(1, lastBracket.length - 2);
                    $(that.wrapSelector('.' + VP_DIR_PARAMETER)).val(parameter);
                    $(that.wrapSelector('.' + VP_DIR_PARAMETER)).show();
                } else {
                    $(that.wrapSelector('.' + VP_DIR_PARAMETER)).val('');
                    $(that.wrapSelector('.' + VP_DIR_PARAMETER)).hide();
                }
            } else {
                $(that.wrapSelector('.' + VP_DIR_PARAMETER)).hide();
            }

            // callback
            if (callback) {
                callback(varObj);
            }
        });

        
    }

    DirBox.prototype.show = function() {
        $(this.wrapSelector()).show();
        this.reload();
    }

    DirBox.prototype.hide = function() {
        $(this.wrapSelector()).hide();
    }

    return DirBox;
})