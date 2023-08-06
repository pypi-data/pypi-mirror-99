define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/pandas/common/commonPandas'
    , 'nbextensions/visualpython/src/pandas/common/pandasGenerator'
    , 'nbextensions/visualpython/src/common/component/vpSuggestInputText'
    // subset editor
    , 'nbextensions/visualpython/src/common/vpSubsetEditor'
    // dir box
    , 'nbextensions/visualpython/src/common/vpDirBox'
    // Code Mirror
    , 'codemirror/lib/codemirror'
    , 'codemirror/mode/python/python'
    , 'notebook/js/codemirror-ipython'
    , 'codemirror/addon/display/placeholder'
    , 'codemirror/addon/display/autorefresh'
], function(requirejs, $, vpCommon, vpConst, sb, vpFuncJS, libPandas, pdGen, vpSuggestInputText
            , vpSubsetEditor, vpDirBox
            , CodeMirror, cmpython, cmip) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "Instance"
        , funcID : "com_instance"
    }

    const MAX_STACK_SIZE = 20;

    var _DATA_TYPES_OF_INDEX = [
        // Index 하위 유형
        'RangeIndex', 'CategoricalIndex', 'MultiIndex', 'IntervalIndex', 'DatetimeIndex', 'TimedeltaIndex', 'PeriodIndex', 'Int64Index', 'UInt64Index', 'Float64Index'
    ]

    var _DATA_TYPES_OF_GROUPBY = [
        // GroupBy 하위 유형
        'DataFrameGroupBy', 'SeriesGroupBy'
    ]

    var _SEARCHABLE_DATA_TYPES = [
        // pandas 객체
        'DataFrame', 'Series', 'Index', 'Period', 'GroupBy', 'Timestamp'
        , ..._DATA_TYPES_OF_INDEX
        , ..._DATA_TYPES_OF_GROUPBY
        // Plot 관련 유형
        //, 'Figure', 'AxesSubplot'
        // Numpy
        //, 'ndarray'
        // Python 변수
        //, 'str', 'int', 'float', 'bool', 'dict', 'list', 'tuple'
    ];

    // function/method types
    var _METHOD_TYPES = ['function', 'method', 'type', 'builtin_function_or_method', 'PlotAccessor'];

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
     var optionLoadCallback = function(callback, meta) {
        // document.getElementsByTagName("head")[0].appendChild(link);
        // 컨테이너에서 전달된 callback 함수가 존재하면 실행.
        if (typeof(callback) === 'function') {
            var uuid = vpCommon.getUUID();
            // 최대 10회 중복되지 않도록 체크
            for (var idx = 0; idx < 10; idx++) {
                // 이미 사용중인 uuid 인 경우 다시 생성
                if ($(vpConst.VP_CONTAINER_ID).find("." + uuid).length > 0) {
                    uuid = vpCommon.getUUID();
                }
            }
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM))).find(vpCommon.formatString(".{0}", vpConst.API_OPTION_PAGE)).addClass(uuid);

            // 옵션 객체 생성
            var varPackage = new VariablePackage(uuid);
            varPackage.metadata = meta;

            // 옵션 속성 할당.
            varPackage.setOptionProp(funcOptProp);
            
            // load metadata
            // if (meta != undefined && meta.options != undefined) {
            //     try {
            //         var leftMeta = decodeURIComponent(meta.options[0].value);
            //         var rightMeta = decodeURIComponent(meta.options[1].value);
                    
            //         var leftBlocks = JSON.parse(leftMeta);
            //         var rightBlocks = JSON.parse(rightMeta);
                    
            //         varPackage.state.left.board.loadBoard(leftBlocks);
            //         varPackage.state.right.board.loadBoard(rightBlocks);
            //     } catch {
            //         ;
            //     }
            // }

            // html 설정.
            varPackage.initHtml();
            callback(varPackage);  // 공통 객체를 callback 인자로 전달
        }
    }
    
    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var initOption = function(callback, meta) {
        vpCommon.loadHtml(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM)), "file_io/instance.html", optionLoadCallback, callback, meta);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var VariablePackage = function(uuid) {
        this.uuid = uuid;   // Load html 영역의 uuid.
        this.package = {
            input: [
                { name: 'vp_instanceVariable' },
                { name: 'vp_instanceAllocate' }
            ]
        }

        this.state = {
            variable: {
                subsetEditor: undefined,
                codeEditor: undefined,
                stack: []
            }
            , allocate: {
                subsetEditor: undefined,
                codeEditor: undefined,
                stack: []
            }
        }
        this.pointer = this.state.variable;

        this.cmconfig = {
            mode: {
                name: 'python',
                version: 3,
                singleLineStringErrors: false
            },  // text-cell(markdown cell) set to 'htmlmixed'
            indentUnit: 4,
            matchBrackets: true,
            autoRefresh: true,
            readOnly: true,
            // lineWrapping: true, // text-cell(markdown cell) set to true
            theme: "default",
            extraKeys: {"Enter": "newlineAndIndentContinueMarkdownList"},
            scrollbarStyle: "null"
        }
    }

    /**
     * vpFuncJS 에서 상속
     */
    VariablePackage.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
     */
    VariablePackage.prototype.optionValidation = function() {
        return true;

        // 부모 클래스 유효성 검사 호출.
        // vpFuncJS.VpFuncJS.prototype.optionValidation.apply(this);
    }

    /**
     * html 내부 binding 처리
     */
    VariablePackage.prototype.initHtml = function() {
        var that = this;
        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "pandas/commonPandas.css");
        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "file_io/instance.css");

        this.bindEvent();

        // variable - codemirror
        this.state.variable.codeEditor = CodeMirror.fromTextArea($(this.wrapSelector('#vp_instanceVariable'))[0], this.cmconfig);
        this.state.variable.codeEditor.setValue('');
        this.state.variable.codeEditor.save();
        // default select variable codemirror
        $('.vp-instance-box.variable .CodeMirror').addClass('selected');

        // allocate - codemirror
        this.state.allocate.codeEditor = CodeMirror.fromTextArea($(this.wrapSelector('#vp_instanceAllocate'))[0], this.cmconfig);
        this.state.allocate.codeEditor.setValue('');
        this.state.allocate.codeEditor.save();

        // load metadata
        var variable = this.getMetadata('vp_instanceVariable');
        var allocate = this.getMetadata('vp_instanceAllocate');
        this.state.variable.codeEditor.setValue(variable);
        this.state.variable.codeEditor.save();
        this.state.allocate.codeEditor.setValue(allocate);
        this.state.allocate.codeEditor.save();

        // vpSubsetEditor
        this.state.variable.subsetEditor = new vpSubsetEditor(this, "vp_instanceVariable", true);
        this.state.allocate.subsetEditor = new vpSubsetEditor(this, "vp_instanceAllocate", true);
        this.state.variable.subsetEditor.hideButton();
        this.state.allocate.subsetEditor.hideButton();

        this.ALLOW_SUBSET_TYPES = that.pointer.subsetEditor.getAllowSubsetTypes();

        // vpDirBox
        this.state.variable.dirBox = new vpDirBox(this, "vp_instanceVariable", 'vp_variableDirContainer');

        // vpDirBox
        this.state.allocate.dirBox = new vpDirBox(this, "vp_instanceAllocate", 'vp_allocateDirContainer');

        that.state.variable.dirBox.show();
        that.state.allocate.dirBox.hide();

        // variable load
        that.reloadDirBox();
    }

    VariablePackage.prototype.bindEvent = function() {
        var that = this;

        // clear
        $(this.wrapSelector('#vp_instanceClear')).click(function(event) {
            that.addStack();
            that.pointer.codeEditor.setValue('');
            that.pointer.codeEditor.save();
            that.reloadDirBox();
        });

        // undo
        $(this.wrapSelector('#vp_instanceUndo')).click(function(event) {
            that.popStack();
            that.reloadDirBox();
        });

        // subset button clicked
        $(document).on('click', this.wrapSelector('.vp-ds-button'), function(event) {
            var dirBoxType = $(this).closest('.vp-instance-box').hasClass('variable')? 'variable': 'allocate';
            $(that.wrapSelector('.CodeMirror')).removeClass('selected');
            if (dirBoxType == 'variable') {
                // variable
                that.state.variable.dirBox.show();
                that.state.allocate.dirBox.hide();
                that.pointer = that.state.variable;
                $(that.wrapSelector('.variable .CodeMirror')).addClass('selected');
            } else if (dirBoxType == 'allocate'){
                // allocate
                that.state.variable.dirBox.hide();
                that.state.allocate.dirBox.show();
                that.pointer = that.state.allocate;
                $(that.wrapSelector('.allocate .CodeMirror')).addClass('selected');
            } else {
                that.state.variable.dirBox.hide();
                that.state.allocate.dirBox.hide();
            }
        });

        // subset applied - variable
        $(document).on('change subset_apply', this.wrapSelector('#vp_instanceVariable'), function(event) {
            var val = $(this).val();
            that.addStack();
            that.state.variable.codeEditor.setValue(val);
            that.state.variable.codeEditor.save();
        });

        // subset applied - allocate
        $(document).on('change subset_apply', this.wrapSelector('#vp_instanceAllocate'), function(event) {
            var val = $(this).val();
            that.addStack();
            that.state.allocate.codeEditor.setValue(val);
            that.state.allocate.codeEditor.save();
        });

        // codemirror clicked
        $(document).on('click', this.wrapSelector('.CodeMirror'), function(event) {
            $(that.wrapSelector('.CodeMirror')).removeClass('selected');
            $(this).addClass('selected');

            // show/hide dirbox
            var dirBoxType = $(this).closest('.vp-instance-box').hasClass('variable')? 'variable': 'allocate';

            if (dirBoxType == 'variable') {
                // variable
                that.state.variable.dirBox.show();
                that.state.allocate.dirBox.hide();
                that.pointer = that.state.variable;
            } else if (dirBoxType == 'allocate'){
                // allocate
                that.state.variable.dirBox.hide();
                that.state.allocate.dirBox.show();
                that.pointer = that.state.allocate;
            } else {
                that.state.variable.dirBox.hide();
                that.state.allocate.dirBox.hide();
            }
        });

        $(document).on('focus', this.wrapSelector('.CodeMirror'), function(event) {
            $(this).trigger('click');
        });
        
        // dirbox selected - variable
        $(document).on('dirbox_selected', this.wrapSelector('#vp_instanceVariable'), function(event) {
            that.addStack();
            
            var nowCode = that.state.variable.codeEditor.getValue();
            if (nowCode != '') {
                nowCode += '.'
            }
            var selectedVariable = event.varName;
            that.state.variable.codeEditor.setValue(nowCode + selectedVariable);
            that.state.variable.codeEditor.save();
            that.reloadDirBox('variable');
        });

        // dirbox selected - allocate
        $(document).on('dirbox_selected', this.wrapSelector('#vp_instanceAllocate'), function(event) {
            that.addStack();
            
            var nowCode = that.state.allocate.codeEditor.getValue();
            if (nowCode != '') {
                nowCode += '.'
            }
            var selectedVariable = event.varName;
            that.state.allocate.codeEditor.setValue(nowCode + selectedVariable);
            that.state.allocate.codeEditor.save();
            that.reloadDirBox('allocate');
        });

        // dirbox_replace - variable
        $(document).on('dirbox_replace', this.wrapSelector('#vp_instanceVariable'), function(event) {
            that.addStack();

            var newCode = event.newCode;
            that.state.variable.codeEditor.setValue(newCode);
            that.state.variable.codeEditor.save();
            that.reloadDirBox('variable');
        });

        // dirbox_replace - allocate
        $(document).on('dirbox_replace', this.wrapSelector('#vp_instanceAllocate'), function(event) {
            that.addStack();

            var newCode = event.newCode;
            that.state.allocate.codeEditor.setValue(newCode);
            that.state.allocate.codeEditor.save();
            that.reloadDirBox('allocate');
        });
    }

    VariablePackage.prototype.addStack = function() {
        var currentValue = this.pointer.codeEditor.getValue();
        this.pointer.stack.push(currentValue);

        // if stack over MAX_STACK_SIZE
        if (this.pointer.stack.length > MAX_STACK_SIZE) {
            this.pointer.stack.splice(0, 1);
        }
        console.log('add stack', currentValue, this.pointer.stack);
    }

    VariablePackage.prototype.popStack = function(replace=true) {
        if (this.pointer.stack.length <= 0) {
            return '';
        }
        
        var lastValue = this.pointer.stack.pop();
        if (replace) {
            this.pointer.codeEditor.setValue(lastValue);
            this.pointer.codeEditor.save();
        }
        console.log('pop stack', lastValue, this.pointer.stack);
        return lastValue;
    }

    VariablePackage.prototype.reloadDirBox = function(type='') {
        var that = this;
        var tempPointer = this.pointer;
        var callbackFunction = function (varObj) {
            var varType = varObj.type;

            if (that.ALLOW_SUBSET_TYPES.includes(varType)) {
                tempPointer.subsetEditor.showButton();
            } else {
                tempPointer.subsetEditor.hideButton();
            }
        };

        if (type == '') {
            this.pointer.dirBox.reload(callbackFunction);
        } else {
            tempPointer = this.state[type];
            this.state[type].dirBox.reload(callbackFunction);
        }
    }

    /**
     * 코드 생성
     * @param {boolean} exec 실행여부
     */
     VariablePackage.prototype.generateCode = function(addCell, exec) {
        var sbCode = new sb.StringBuilder();

        // 변수 내용 조회
        var leftCode = this.state.allocate.codeEditor.getValue();
        var rightCode = this.state.variable.codeEditor.getValue();
        if (leftCode && leftCode != '') {
            sbCode.appendFormat('{0} = {1}', leftCode, rightCode);
        } else {
            sbCode.appendFormat('{0}', rightCode);
        }

        if (addCell) this.cellExecute(sbCode.toString(), exec);

        return sbCode.toString();
    }

    return {
        initOption: initOption
    };
})