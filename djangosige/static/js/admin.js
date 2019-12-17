if (typeof jQuery === "undefined") {
    throw new Error("Carregar JQuery antes deste arquivo.");
}

$.Admin = {};

//Barra lateral
$.Admin.barraLateral = {
    init: function() {
        var _this = this;
        var $body = $('body');
        var $overlay = $('.overlay');

        //Fecha barra lateral ao clicar na tela
        $(window).click(function (e) {
            var $target = $(e.target);
            if (e.target.nodeName.toLowerCase() === 'i') { $target = $(e.target).parent(); }
            if (!$target.hasClass('bars') && _this.isOpen() && $target.parents('#barralateral').length === 0 && !$target.hasClass('dropdown-backdrop')) {
                $overlay.fadeOut();
                $body.removeClass('overlay-open');
            }
        });

        //Determina o tamanho das barras
        _this.checkStatuForResize(true);
        $(window).resize(function () {
            _this.checkStatuForResize(false);
        });

        //Esconde|expande itens com lista da barra lateral
        $('.menu-toggle').on('click', function (e) {
            var $this = $(this);
            var $content = $this.next();

            if ($($this.parents('ul')[0]).hasClass('list')) {
                var $not = $(e.target).hasClass('menu-toggle') ? e.target : $(e.target).parents('.menu-toggle');

                $.each($('.menu-toggle.toggled').not($not).next(), function (i, val) {
                    if ($(val).is(':visible')) {
                        $(val).prev().toggleClass('toggled');
                        $(val).slideUp();
                    }
                });
            }

            $this.toggleClass('toggled');
            $content.slideToggle(320);
        });

        //Popups
        $('a.popup, tr.popup').on('click', function(event){

            if(!$(event.target).is("input, label")){
                var w = '600'
                var h = '500'
                var dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : screen.left;
                var dualScreenTop = window.screenTop != undefined ? window.screenTop : screen.top;

                var width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
                var height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

                var left = ((width / 2) - (w / 2)) + dualScreenLeft;
                var top = ((height / 2) - (h / 2)) + dualScreenTop;
                if($(this).prop('href')){
                    newwindow = window.open($(this).prop('href'), $(this).prop('title'), 'scrollbars=yes, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);
                }else{
                    newwindow = window.open($(this).attr('href'), $(this).attr('title'), 'scrollbars=yes, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);
                }
                if (window.focus) {newwindow.focus()}

                return false;
            }
        });

        //New Window
        $('a.newwindow, tr.newwindow').on('click', function(event){
            window.open($(this).prop('href'), $(this).prop('title'));
            return false;
        });
    },

    checkStatuForResize: function (firstTime) {
        var $body = $('body');
        var $openCloseBar = $('.navbar .navbar-header .bars');
        var width = $body.width();

        if (firstTime) {
            $body.find('.content, .sidebar').addClass('no-animate').delay(1000).queue(function () {
                $(this).removeClass('no-animate').dequeue();
            });
        }
        if (width < 1170) {
            $body.addClass('ls-closed');
            $openCloseBar.fadeIn();
        }
        else {
            $body.removeClass('ls-closed');
            $openCloseBar.fadeOut();
        }
    },
    isOpen: function () {
        return $('body').hasClass('overlay-open');
    }
}

// Navbar
$.Admin.navbar = {
    init: function () {
        var $body = $('body');
        var $overlay = $('.overlay');

        //Abre|fecha barra lateral
        $('.bars').on('click', function () {
            $body.toggleClass('overlay-open');
            if ($body.hasClass('overlay-open')) { $overlay.fadeIn(); } else { $overlay.fadeOut(); }
        });
    }
}

//Mensagens
$.Admin.messages = {
    //Mensagens sucesso
    msgSucesso: function(message){
        $('#modal-msg .modal-header span i').text('done').addClass('icon-success');
        $('#modal-msg .modal-body p').text(message);
        $('#modal-msg .modal-title').text('Sucesso');
        $('#modal-msg').modal('show');
        $('#modal-msg #btn-ok').show();
        $('#modal-msg #btn-sim').hide();
        $('#modal-msg #btn-nao').hide();
    },

    //Mensagem pergunta antes de remover
    msgRemove: function(message){
        $('#modal-msg .modal-header span i').text('error_outline').addClass('icon-alert');
        $('#modal-msg .modal-body p').text(message);
        $('#modal-msg .modal-title').text('Tem certeza?');
        $('#modal-msg').modal('show');
        $('#modal-msg #btn-sim').show();
        $('#modal-msg #btn-nao').show();
        $('#modal-msg #btn-ok').hide();
    },

    //Mensagem operação não permitida
    msgAlerta: function(message){
        $('#modal-msg .modal-header span i').text('error_outline').addClass('icon-alert');
        $('#modal-msg .modal-body p').text(message);
        $('#modal-msg .modal-title').text('Operação não permitida');
        $('#modal-msg').modal('show');
        $('#modal-msg #btn-ok').show();
        $('#modal-msg #btn-sim').hide();
        $('#modal-msg #btn-nao').hide();
    }
}

//DataTable
$.Admin.table = {
    init: function() {
        var $btnRemove = $('.btn-remove');

        //Auto detect dates (dd/mm/yyyy) for sorting
        $.fn.dataTableExt.aTypes.unshift(
            function ( sData )
            {
                if (sData !== null && sData.match(/^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[012])\/(19|20|21)\d\d$/))
                {
                    return 'date-uk';
                }
                return null;
            }
        );

        //Sort dates (dd/mm/yyyy)
        jQuery.extend( jQuery.fn.dataTableExt.oSort, {
            "date-uk-pre": function ( a ) {
                if (a == null || a == "") {
                    return 0;
                }
                var ukDatea = a.split('/');
                return (ukDatea[2] + ukDatea[1] + ukDatea[0]) * 1;
            },

            "date-uk-asc": function ( a, b ) {
                return ((a < b) ? -1 : ((a > b) ? 1 : 0));
            },

            "date-uk-desc": function ( a, b ) {
                return ((a < b) ? 1 : ((a > b) ? -1 : 0));
            }
        } );

        //Tabela DataTable
        dTable = $('#lista-database').DataTable({
            "dom" : 'ltipr',
            "language" : {
                "sEmptyTable": "Nenhum registro encontrado",
                "sInfo": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
                "sInfoEmpty": "Mostrando 0 até 0 de 0 registros",
                "sInfoFiltered": "(Filtrados de _MAX_ registros)",
                "sInfoPostFix": "",
                "sInfoThousands": ".",
                "sLengthMenu": "Mostrar _MENU_ resultados por página",
                "sLoadingRecords": "Carregando...",
                "sProcessing": "Processando...",
                "sZeroRecords": "Nenhum registro encontrado",
                "sSearch": "Pesquisar",
                "oPaginate": {
                    "sNext": "Próximo",
                    "sPrevious": "Anterior",
                    "sFirst": "Primeiro",
                    "sLast": "Último"
                },
                "oAria": {
                    "sSortAscending": ": Ordenar colunas de forma ascendente",
                    "sSortDescending": ": Ordenar colunas de forma descendente"
                },
            }
        });

        //Campo de busca
        $('#search-bar').keyup(function(){
            dTable.search($(this).val()).draw();
        });

        //Mudar o background do tr quando remover for selecionado
        $('body').on('change', '.lista-remove input[type=checkbox]', function(event){
            if(this.checked){
                $(this).parents('tr').addClass("delete-row");
            }else{
                $(this).parents('tr').removeClass("delete-row");
            }
            $btnRemove.show()
        });

        //Perguntar antes de remover items da database
        $btnRemove.on('click',function(event){
            event.preventDefault();
            var form = $(this).parents('form');
            $.Admin.messages.msgRemove("Os items selecionados serão removidos permanentemente da Base de Dados.");
            $('#btn-sim').one('click', function(){
                form.submit();
            });
        });

        //Fazer a linha da table um link para a detail view
        $('body').on('click', '.clickable-row:not(.popup)', function(event){
            if(!$(event.target).is("input, label, i, .prevent-click-row")){
                window.document.location = $(this).data("href");
            }
        });

    },
}

//Formsets
$.Admin.formset = {
    init: function() {
        var _this = this;
        var $formset_box = $('.formset-box');

        $formset_box.each(function(){
            var currentBox = $(this);
            var formsetPrefix = currentBox.find('.formset:last').prop('id');
            var nFormsets = (parseInt(formsetPrefix.substring(formsetPrefix.indexOf('-') + 1), 10) + 1).toString();

            formsetPrefix = formsetPrefix.substring(0, formsetPrefix.indexOf('-'));

            //Esconder campo DELETE do Django
            currentBox.find('.formset').each(function(){
                _this.hideDeleteField($(this))
            });

            //Esconder botao adicionar novo dos formularios, excluindo o ultimo
            currentBox.find('.formset:not(:last)').each(function(){
                $(this).find('.add-formset').hide();
            });

            //Adicionar novo formset
            currentBox.on('click', '.add-formset', function(e){
                e.preventDefault();
                var parentFormset = $(this).parents('.formset');
                _this.createNewForm(parentFormset, nFormsets);

                //Adicionar form ao manager
                nFormsets++;
                $('#id_' + formsetPrefix + '-TOTAL_FORMS').val(nFormsets);

                //Esconder add e remove do penultimo form
                $(this).hide();
                parentFormset.next().trigger('formCreated');
            });

            //Remover formset
            currentBox.on('click', '.remove-formset', function(e){
                e.preventDefault();
                var parentFormset = $(this).parents('.formset');
                var entryId = parentFormset.find('input:hidden[id $="-id"],input:hidden[id $="grupo_ptr"]');

                if(entryId.length){
                    parentFormset.find('input:checkbox[id $="-DELETE"]').prop('checked', true);
                }else{
                    parentFormset.find(':input').each(function(){
                        $(this).prop({'value': ''}).val('').prop('checked',false);
                    });
                    parentFormset.find('input:checkbox[id $="-DELETE"]').prop('checked', true);
                    parentFormset.trigger('newFormRemoved');
                }
                parentFormset.hide().change();

                var addBtn = currentBox.find('.formset:visible:last .add-formset');

                if(!addBtn.length){
                    _this.createNewForm(parentFormset, nFormsets);
                    //Adicionar form ao manager
                    nFormsets++;
                    $('#id_' + formsetPrefix + '-TOTAL_FORMS').val(nFormsets);
                }else{
                    addBtn.show();
                }

                parentFormset.trigger('formRemoved');
            });
        });
    },

    hideDeleteField: function(formset){
        var delete_input = formset.find('input:checkbox[id $="-DELETE"]');
        var delete_td = delete_input.parent('.field-td');

        delete_input.parents('.form-group:first').parent('div').hide();

        delete_td.closest('table').find('th').eq(delete_td.index()).hide();
        delete_td.hide();
    },

    createNewForm: function(parentFormset, nFormsets){
        var newForm = parentFormset.clone(true);

        //Trocar id
        var nameRegex = /-\d+-?/g;
        var newId = newForm.prop('id').replace(nameRegex, '-' + (nFormsets));
        newForm.prop({'id':newId});

        //Trocar names e ids dos inputs
        newForm.find(':input').each(function(){
            var newName = $(this).prop('name');
            if($(this).prop('type') == 'hidden'){
                $(this).remove();
            }
            //Remover mask do clone, senao nao funciona com novos inputs!
            $(this).removeData('mask');

            if(newName){
                newName = newName.replace(nameRegex, '-' + (nFormsets) + '-');
                var newId = 'id_' + newName;
                $(this).prop({'name': newName, 'id': newId, 'value': ''}).val('');

                if($(this).prop('type') == 'checkbox'){
                    $(this).prop({'checked': false}).removeProp('value').removeAttr('value');
                }
            }

        });

        //Trocar atributos for dos labels
        newForm.find('label').each(function() {
            var newFor = $(this).prop('for');
            if(newFor){
                newFor = newFor.replace(nameRegex,'-' + nFormsets + '-');
                $(this).prop({'for': newFor});
            }

            if($(this).hasClass('error')){
                $(this).remove();
            }
        });
        newForm.show();
        newForm.insertAfter(parentFormset);
    },

    createNewTrForms: function(table, n_new_forms){
        var startFrom = 0;
        table.find('tbody tr').each(function(){
            var table_row = $(this);
            var entryId = table_row.find('input:hidden[id $="-id"]');

            if(entryId.length){
                table_row.find('input:checkbox[id $="-DELETE"]').prop('checked', true);
                startFrom++;
                table_row.addClass('hidden');
            }else{
                table_row.remove();
            }
        });

        if(typeof n_new_forms != 'undefined' || n_new_forms){
            var formsetPrefix = table.find('tbody tr').eq(0).prop('id');
            formsetPrefix = formsetPrefix.substring(0, formsetPrefix.indexOf('-'));

            for (i = 0; i < parseInt(n_new_forms); i++) {
                if(startFrom <= 0){
                    var trClones = table.find('tbody tr').eq(0).removeClass('hidden').clone(true);
                }else{
                    var trClones = table.find('tbody tr').eq(startFrom-1).clone(true);
                    trClones.removeClass('hidden');
                }

                var nameRegex = /-\d+-?/g;

                trClones.each(function(){
                    var nameIdNumber = i + startFrom;
                    var newId = $(this).prop('id').replace(nameRegex, '-' + (nameIdNumber));

                    $(this).prop({'id':newId});

                    $(this).find('input').each(function(){
                        var newName = $(this).prop('name');
                        if($(this).prop('type') == 'hidden'){
                            $(this).remove();
                        }

                        //Remover mask do clone, senao nao funciona com novos inputs!
                        $(this).removeData('mask');
                        //Desfazer datepicker
                        if($(this).hasClass('datepicker')){
                            $(this).datepicker('destroy').removeAttr('id').removeProp('id');
                        }

                        if(newName){
                            newName = newName.replace(nameRegex, '-' + (nameIdNumber) + '-');
                            var newId = 'id_' + newName;
                            $(this).prop({'name': newName, 'id': newId, 'value': ''}).val('').prop('checked',false);
                        }
                    });

                    $(this).appendTo(table.find('tbody'));
                });
            }

            //Adicionar form ao manager
            $('#id_' + formsetPrefix + '-TOTAL_FORMS').val(parseInt(n_new_forms) + startFrom);
        }
    },
}

$.Admin.validation = {
    init: function() {
        //Mudar tab quando campo invalido
        $('.tab-pane input, .tab-pane textarea, .tab-pane select').on('invalid', function(){
           var $closest = $(this).closest('.tab-pane');
           var id = $closest.prop('id');
           $('.nav a[href="#' + id + '"]').tab('show');
        });

        $(".tab-content").find("div.tab-pane:hidden:has(td.form-td-error,label.error)").each(function(index, tab){
            var id = $(tab).prop("id");
            $('a[href="#' + id + '"]').tab('show');
        });
    }
}


$.Admin.maskInput = {
    maskEmpresa: function() {
        $('input[name$="cnpj"]').mask('99.999.999/9999-99', {reverse: true});
        $(document).on('focus', 'input[name$="-telefone"]', function(){
            $(this).mask('(99) 9999-9999A', {translation:{'A': {pattern: /[0-9]/, optional: true}}}).focusout(function (event) {
                var target, phone, element;
                target = (event.currentTarget) ? event.currentTarget : event.srcElement;
                phone = target.value.replace(/\D/g, '');
                element = $(target);
                element.unmask();
                if(phone.length > 10) {
                    element.mask("(99) 99999-999A", {translation:{'A': {pattern: /[0-9]/, optional: true}}});
                } else {
                    element.mask("(99) 9999-9999A", {translation:{'A': {pattern: /[0-9]/, optional: true}}});
                }
            });
        });
    },

    maskPessoa: function() {
        $('input[name$="cnpj"]').mask('99.999.999/9999-99', {reverse: true});
        $('input[name$="cpf"]').mask('999.999.999-99', {reverse: true});
        $('.decimal-mask').mask('000.000.000.000,00', {reverse: true});
        $(document).on('focus', 'input[name$="-telefone"]', function(){
            $(this).mask('(99) 9999-9999A', {translation:{'A': {pattern: /[0-9]/, optional: true}}}).focusout(function (event) {
                var target, phone, element;
                target = (event.currentTarget) ? event.currentTarget : event.srcElement;
                phone = target.value.replace(/\D/g, '');
                element = $(target);
                element.unmask();
                if(phone.length > 10) {
                    element.mask("(99) 99999-999A", {translation:{'A': {pattern: /[0-9]/, optional: true}}});
                } else {
                    element.mask("(99) 9999-9999A", {translation:{'A': {pattern: /[0-9]/, optional: true}}});
                }
            });
        });
    },

    maskProduto: function() {
        $('.decimal-mask').mask('000.000.000.000,00', {reverse: true});
    },

    maskGrupoFiscal: function(){
        $('.percentual-mask').mask('000,00', {reverse: true});
        $('.decimal-mask').mask('000.000.000.000,00', {reverse: true});
        $('#id_ipi_form-cnpj_prod').mask('99.999.999/9999-99', {reverse: true});
    },

    maskNotaFiscal: function(){
        $('.percentual-mask').mask('000,00', {reverse: true});
        $('.decimal-mask').mask('000.000.000.000,00', {reverse: true});
        $('.decimal-mask-no-dot').mask('000000000000,00', {reverse: true});
        $('#id_n_nf').mask('000000000', {reverse: true});
    },

    maskVenda: function(){
        $('.decimal-mask').mask('000.000.000.000,00', {reverse: true});
        $('.decimal-mask-no-dot').mask('000000000000,00', {reverse: true});
        $('.decimal-mask-four').mask('000.000.000,00DD', {reverse: true, translation:{'D': {pattern: /[0-9]/, optional: true}}});
        $('.percentual-mask').mask('000,00', {reverse: true});
    },

    maskLancamento: function(){
        $('.decimal-mask').mask('000.000.000.000,00', {reverse: true});
        $('.percentual-mask').mask('000,00', {reverse: true});
        $('.datepicker').mask('00/00/0000', {reverse: true});
    },

    maskFatura: function(){
        $('.decimal-mask').mask('000.000.000.000,00', {reverse: true});
        $('.datepicker').mask('00/00/0000', {reverse: true});
    },

    maskMovimentoEstoque: function(){
        $('.decimal-mask').mask('000.000.000.000,00', {reverse: true});
        $('.datepicker').mask('00/00/0000', {reverse: true});
    }
}


$.Admin.pessoaForm = {
    init: function(cmun_path, mun_inicial) {
        var _this = this;
        _this.trocarCampos();

        $('input[type="radio"][name$="tipo_pessoa"]').change(function(){
            _this.trocarCampos($(this));
        });

        $('.formset').on('change', 'select[id$=-uf]', function(event, mun_inicial){
            var form_number = $(this).prop('id').match(/\d/)[0];
            var mun_input = $("#id_endereco_form-" + form_number + "-municipio");
            mun_input.empty();
            if($(this).val() && $(this).val() != 'EX'){
                file_path = cmun_path + $(this).val() + '.csv'
                $.ajax({
                    type: "GET",
                    url: file_path,
                    dataType: "text",
                    success: function(data){_this.processCmunData(data, mun_input, mun_inicial);}
                });
            }
        });

        if(mun_inicial.length){
            $('select[id$=-uf').each(function(index){
                $(this).trigger('change', mun_inicial[index]);
            });
        }

        $('body').on('change', 'select[id$=-municipio]', function(){
            var form_number = $(this).prop('id').match(/\d/)[0];
            var cmun_input = $("#id_endereco_form-" + form_number + "-cmun");
            var cmun = $(this).find('option:selected').text().match(/\((.*)\)/);
            cmun_input.val(cmun[1]);
        });
    },

    trocarCampos: function (chkBox) {
        if (typeof chkBox != 'undefined'){
            var chkId = chkBox.prop('id');
            if(chkId=='fisica'){
                $('.pessoa_jur_form').hide();
                $('.pessoa_fis_form').show();
            }else if(chkId=='juridica'){
                $('.pessoa_jur_form').show();
                $('.pessoa_fis_form').hide();
            }
        }else{
           if($('input[id="fisica"]').is(':checked')){
                $('.pessoa_jur_form').hide();
                $('.pessoa_fis_form').show();
            }else if($('input[id="juridica"]').is(':checked')){
                $('.pessoa_jur_form').show();
                $('.pessoa_fis_form').hide();
            }
        }
    },

    processCmunData: function(data, mun_input, mun_inicial){
        var lines = data.split(/\r\n|\n/);
        for(var i=1; i<lines.length; i++){
            line = lines[i].split(',');
            var cod_mun = line[0];
            var mun = line[1];

            if(mun){
                var option = $('<option></option>').prop("value", mun).text(mun+' ('+ cod_mun +')');
                mun_input.append(option);
            }
        }
        if(mun_inicial){
            mun_input.val(mun_inicial);
        }else{
            mun_input.change();
        }
    },
}

$.Admin.popupwindow = {
    init: function() {

        //Adicionar a base de dados, redirecionamento
        $('a.popup-add').on('click', function(){
            window.opener.location = $(this).prop('href');
            window.close();
        });

        //Fecha popup quando form submit
        $('#popupform').submit(function(ev) {
            ev.preventDefault();
            $.ajax({
                type: "POST",
                url: "",
                data: $(this).serialize(),
                success: function() {
                    window.opener.location.reload(true);
                    window.close();
               }
            });
        });

    },
}


$.Admin.produtoForm = {
    init: function(ncm_path) {
        var _this = this;
        $.Admin.autocompleteField.autocompleteNcm(ncm_path);

        _this.setMargemLucro();
        $('.tab-content').find('input[name^="custo"][type="text"], input[name^="venda"][type="text"]').each(function(i){
            $(this).blur(function(e){
                _this.setMargemLucro();
            })
        });

        //Remover(readonly) campos de controle de estoque caso o usuario prefira nao controlar o estoque.
        $('#id_controlar_estoque').on('change', function(){
            var chkBox = $(this).is(':checked');
            $('#estoque_fields').find('input[type=text],select').each(function(){
                if(chkBox){
                    $(this).prop('readonly', false);
                    $(this).removeClass('input_no_edit');
                }else{
                    $(this).prop('readonly', true);
                    $(this).addClass('input_no_edit');
                    if($(this).is('select')){
                        $(this).val('');
                    }else{
                        $(this).val('0,00');
                    }
                }
            });

        });
    },

    setMargemLucro: function(){
        if($('input[name^="custo"]').val()!="" && $('input[name^="venda"]').val()!=""){
            var textoVenda = $('input[name^="venda"]').val();
            textoVenda = textoVenda.replace(/\./g,"").replace(",",".");
            var textoCusto = $('input[name^="custo"]').val();
            textoCusto = textoCusto.replace(/\./g,"").replace(",",".");
            var venda = parseFloat(textoVenda).toFixed(2);
            var custo = parseFloat(textoCusto).toFixed(2);
            var margem = ((venda-custo)/venda)*100;
            $('.tab-content').find('span[id="margem-lucro"]').text(parseFloat(margem).toFixed(2)+"%");
        }else{
            $('.tab-content').find('span[id="margem-lucro"]').text('0%');
        }
    },
}


$.Admin.grupoFiscalForm = {
    init: function() {
        var _this = this;
        regimeField = $('#id_regime_trib');
        icmsCstField = $('#id_icms_form-cst');
        icmssnCsosnField = $('#id_icmssn_form-csosn');
        tipoIpiField = $('#id_ipi_form-tipo_ipi');
        pisCstField = $('#id_pis_form-cst');
        cofinsCstField = $('#id_cofins_form-cst');

        _this.escondeCamposIcms(icmsCstField);
        _this.escondeCamposIcmsSn(icmssnCsosnField);
        _this.escondeCamposRegime(regimeField);
        _this.escondeCamposIpi(tipoIpiField);
        _this.escondeCamposPis(pisCstField);
        _this.escondeCamposCofins(cofinsCstField);

        icmsCstField.on('change', function(){
            _this.escondeCamposIcms($(this));
        });

        icmssnCsosnField.on('change', function(){
            _this.escondeCamposIcmsSn($(this));
        });

        regimeField.on('change', function(){
            _this.escondeCamposRegime($(this));
        });

        tipoIpiField.on('change', function(){
            _this.escondeCamposIpi($(this));
        });

        pisCstField.on('change', function(){
            _this.escondeCamposPis($(this));
        });

        cofinsCstField.on('change', function(){
            _this.escondeCamposCofins($(this));
        });


    },
    //esconde campos de acordo com a escolha do CST do ICMS
    escondeCamposIcms: function (icmsCstField) {
        var fieldValue = icmsCstField.find(":selected").val();
        $('.icms_form:not(.icms-cst):not(.calculo-icms)').addClass('hidden');
        $('.icms' + fieldValue).removeClass('hidden');
    },

    //esconde campos de acordo com a escolha do CSOSN
    escondeCamposIcmsSn: function (icmssnCsosnField) {
        var fieldValue = icmssnCsosnField.find(":selected").val();
        $('.icmssn_form:not(.icmssn-csosn):not(.calculo-icmssn)').addClass('hidden');
        $('.icmssn' + fieldValue).removeClass('hidden');
    },

    //Esconde os campos dependendo da situacao tributaria
    escondeCamposRegime: function (regimeField) {
        var fieldValue = regimeField.find(":selected").val();

        //Simples nacional==1 ou tributação normal==0
        if(fieldValue == '1'){
            $('.icmssn_form').show();
            $('.icms_form').hide();
        }else if(fieldValue == '0'){
            $('.icmssn_form').hide();
            $('.icms_form').show();
        }
    },

    escondeCamposIpi: function(tipoIpiField){
        var fieldValue = tipoIpiField.find(":selected").val();
        //Nao sujeito
        if(fieldValue == '0'){
            $('#id_ipi_form-p_ipi').parents('div').eq(2).hide();
            $('#id_ipi_form-valor_fixo').parents('div').eq(2).hide();
        //Valor fixo
        }else if(fieldValue == '1'){
            $('#id_ipi_form-p_ipi').parents('div').eq(2).hide();
            $('#id_ipi_form-valor_fixo').parents('div').eq(2).show();
        //Aliquota
        }else if(fieldValue == '2'){
            $('#id_ipi_form-p_ipi').parents('div').eq(2).show();
            $('#id_ipi_form-valor_fixo').parents('div').eq(2).hide();
        }
    },

    escondeCamposPis: function(cstField){
        var fieldValue = cstField.find(':selected').val();
        if (fieldValue == '01' || fieldValue == '02'){
            $('#id_pis_form-p_pis').parents('div').eq(2).show();
            $('#id_pis_form-valiq_pis').val('').parents('div').eq(2).hide();
        }else if(fieldValue == '03'){
            $('#id_pis_form-p_pis').val('').parents('div').eq(2).hide();
            $('#id_pis_form-valiq_pis').parents('div').eq(2).show();
        }else if(['04', '05', '06', '07', '08', '09'].indexOf(fieldValue) +1){
            $('#id_pis_form-p_pis').val('').parents('div').eq(2).hide();
            $('#id_pis_form-valiq_pis').val('').parents('div').eq(2).hide();
        }else{
            $('#id_pis_form-p_pis').parents('div').eq(2).show();
            $('#id_pis_form-valiq_pis').parents('div').eq(2).show();
        }
    },

    escondeCamposCofins: function(cstField){
        var fieldValue = cstField.find(':selected').val();
        if (fieldValue == '01' || fieldValue == '02'){
            $('#id_cofins_form-p_cofins').parents('div').eq(2).show();
            $('#id_cofins_form-valiq_cofins').val('').parents('div').eq(2).hide();
        }else if(fieldValue == '03'){
            $('#id_cofins_form-p_cofins').val('').parents('div').eq(2).hide();
            $('#id_cofins_form-valiq_cofins').parents('div').eq(2).show();
        }else if(['04', '05', '06', '07', '08', '09'].indexOf(fieldValue) +1){
            $('#id_cofins_form-p_cofins').val('').parents('div').eq(2).hide();
            $('#id_cofins_form-valiq_cofins').val('').parents('div').eq(2).hide();
        }else{
            $('#id_cofins_form-p_cofins').parents('div').eq(2).show();
            $('#id_cofins_form-valiq_cofins').parents('div').eq(2).show();
        }
    },
}

$.Admin.autocompleteField = {
    autocompleteNcm: function(ncm_path) {
        var _this = this;
        $.ajax({
            type: "GET",
            url: ncm_path,
            dataType: "text",
            success: function(data){_this.processNcmData(data);}
        });
    },

    processNcmData: function(data) {
        var ncm_input = $( "#id_ncm" )
        var ncm = []
        var lines = data.split(/\r\n|\n/);
        for(var i=1; i<lines.length; i++){
            line = lines[i].split(';');
            var cod_ncm = line[0];
            var desc = line[2];

            if(line[1] != ''){
                cod_ncm = cod_ncm + '[EX:'+ line[1]+']';
            }
            ncm.push({value:cod_ncm, label:cod_ncm+' - '+desc});
        }

        ncm_input.autocomplete({
            minLength:4,
            source: ncm,
            messages: {
                noResults:'',
                results:function(){}
            }
        });

        //manter dropdown mesmo tamanho do input
        $('.ui-menu').css('max-width', $(window).width()/2);
    },

    autocompleteCfop: function(cfop_path) {
        var _this = this;
        $.ajax({
            type: "GET",
            url: cfop_path,
            dataType: "text",
            success: function(data){_this.processCfopData(data);}
        });
    },

    processCfopData: function (data) {
        var cfop_input = $( "#id_cfop" );
        var cfop_desc_input = $("#id_descricao");
        var text_cfop = []
        var text_desc = []
        var lines = data.split(/\r\n|\n/);
        for(var i=1; i<lines.length; i++){
            line = lines[i].split(';');
            var cop_cfop = line[0];
            var desc = line[1];

            text_cfop.push({value:cop_cfop, label:cop_cfop+' - '+desc});
            text_desc.push({value:desc, label:cop_cfop+' - '+desc});
        }

        cfop_input.autocomplete({
            minLength:1,
            source: text_cfop,
            select: function(event, ui){
                cfop_desc_input.val(ui.item.label.substring(7))
                setTipoOperacao(ui.item.label.substring(0,1));
            },
            messages: {
                noResults:'',
                results:function(){}
            }
        });

        cfop_desc_input.autocomplete({
            minLength:4,
            source: text_desc,
            select: function(event, ui){
                cfop_input.val(ui.item.label.substring(0,4));
                setTipoOperacao(ui.item.label.substring(0,1));
            },
            messages: {
                noResults:'',
                results:function(){}
            }
        });

        function setTipoOperacao(cfop_indice){
            if(cfop_indice == '1' ||
               cfop_indice == '2' ||
               cfop_indice == '3'){
                   $("#id_tp_operacao").val('0');
           }
            else if(cfop_indice == '5' ||
               cfop_indice == '6' ||
               cfop_indice == '7'){
                   $("#id_tp_operacao").val('1');
           }
        }
    },

    autocompleteCest: function(cest_path) {
        var _this = this;
        $.ajax({
            type: "GET",
            url: cest_path,
            dataType: "text",
            success: function(data){_this.processCestData(data);}
        });
    },

    processCestData: function (data) {
        var cest_input = $( "#id_cest" )
        var text = []
        var lines = data.split(/\r\n|\n/);
        for(var i=1; i<lines.length; i++){
            line = lines[i].split(';');
            var cod_cest = line[0];
            var desc = line[1];

            text.push({value:cod_cest, label:cod_cest+' - '+desc});
        }

        cest_input.autocomplete({
            minLength:3,
            source: text,
            messages: {
                noResults:'',
                results:function(){}
            }
        });

        //manter dropdown mesmo tamanho do input
        $('.ui-menu').css('max-width', $(window).width()/2);
    },
}


$.Admin.vendaForm = {
    init: function(req_urls) {
        var _this = this;
        var cli_input = $('#id_cliente');
        var transportadora_input = $('#id_transportadora')
        var cond_pag_input = $('#id_cond_pagamento');
        var produtos_input = $('select.select-produto');

        $.Admin.maskInput.maskVenda();
        //Preencher campos edit view
        $('#id_valor_total_display').text($('#id_valor_total').val());

        $('.formset[id^=produtos_form-]').each(function(){
            var form_number = $(this).prop('id').match(/\d/)[0];
            if($(this).find('select[id$=-produto]').val().length === 0){
                _this.setInitialItensData($(this));
            }
            _this.hideModalFields($(this));
            if($('#venda_form_add').length) _this.setItensFields(form_number);
        });

        _this.formTableInit();
        _this.alterarFieldsModal(true);

        $(document).on('focus', '.decimal-mask', function(){
            $.Admin.maskInput.maskVenda();
        });

        cli_input.on('change', function(){
            if($(this).val()){
                var postData = {
                    'pessoaId': $(this).val(),
                }
                $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_cliente_url'], postData, _this.handleClienteInfo);
            }else{
                _this.handleClienteInfo();
            }
        });

        cli_input.change();

        transportadora_input.on('change', function(){
            if($(this).val()){
                var postData = {
                    'transportadoraId': $(this).val(),
                }
                $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_transportadora_url'], postData, _this.handleTransportadoraInfo);
            }else{
                _this.handleTransportadoraInfo();
            }
        });

        transportadora_input.change();

        cond_pag_input.on('change', function(event, initial){
            if($(this).val()){
                var postData = {
                    'pagamentoId': $(this).val(),
                }
                $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_pagamento_url'], postData, _this.handlePagamentoInfo, initial);
            }else{
                _this.handlePagamentoInfo(null, initial);
            }
        });

        cond_pag_input.trigger('change', [true]);

        produtos_input.on('change', function(event, initial){
            var form_number = $(this).prop('id').match(/\d/)[0];
            if($(this).val()){
                var postData = {
                    'produtoId': $(this).val(),
                }
                $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_produto_url'], postData, _this.handleProdutoInfo, form_number, initial);
            }else{
                _this.handleProdutoInfo(null, form_number, initial);
            }
        });

        produtos_input.trigger('change', [true]);

        /*  Eventos  */

        //Caso campo esteja vazio manter 0
        $(document).on('change keyup', 'input[id$=-quantidade],input[id$=-valor_unit],input[id$=desconto],input[id$=frete],input[id$=despesas],input[id$=seguro],.imposto_modal .decimal-mask,.imposto_modal .decimal-mask-no-dot', function(){
            if(!$(this).val()) $(this).val('0');
        });

        //Ratear valores
        $('#ratear_valores_btn').on('click', function(){
            _this.ratearValores();
        });

        //Atualiza valor total por item e adicionais totais
        $(document).on('load change keyup paste', 'input[id$=-quantidade],input[id$=-valor_unit],select[id$=-tipo_desconto],input[id$=-desconto],input[id$=-valor_rateio_frete],input[id$=-valor_rateio_despesas],input[id$=-valor_rateio_seguro]', function(){
            var form_number = $(this).prop('id').match(/\d/)[0];
            _this.setItensFields(form_number);
            _this.setAdicionaisTotal();
            $('#id_desconto').change();
        });

        //Atualiza o desconto total ao trocar o tipo de desconto
        $(document).on('change', '#id_tipo_desconto', function(){
            _this.setAdicionaisTotal();
        });

        //Atualiza o valor total da venda ao modificar o total dos itens, ou qualquer campo total(tipo_desconto, desconto, frete, etc.)
        $(document).on('change keyup paste', 'input[id$=-subtotal],#id_tipo_desconto,#id_desconto,#id_frete,#id_despesas,#id_seguro', function(){
            _this.setTotalFields();
        });

        //Atualiza o desconto total e o valor total da venda ao deletar formsets.
        $('.formset').on('change', function(){
            _this.setAdicionaisTotal();
            _this.setTotalFields();
        });

        //Preencher data inicial dos forms criados (para ItensVenda)
        $('.formset').on('formCreated', function(){
            _this.setInitialItensData($(this));
        });

        //Mostrar modal do imposto ao clicar no icone
        $('.imposto-icon').on('click', function(){
            _this.mostrarModalImposto($(this).parents('.formset'));
        });

        //Alterar campos imposto, dependendo da opcao de calculo automatico
        $('#id_auto_calcular_modal').on('change', function(){
            _this.alterarFieldsModal($(this).is(':checked'));
        });

        $('#calcular-parcelas').on('click', function(){
            _this.setTotalParcelasFields();
        });

        $('#salvar_impostos_modal').on('click', function(){
            _this.salvarInfoImpostoModal($(this).parents('.imposto_modal'));
        });

        $('#venda_form_edit, #venda_form_add').on('submit', function(){
            return _this.verificarParcelas();
        });

        //Abrir pdf em nova tab
        $('#gerar_pdf_venda').on('click', function(event){
            event.preventDefault();
            window.open($(this).prop('href'), $(this).prop('title'));
            return false;
        });
    },

    setInitialItensData: function(prod_formset){
        prod_formset.find('input[id$=-quantidade]').val(1);
        prod_formset.find('input[id$=-valor_unit]').val('0,00');
        prod_formset.find('select[id$=-tipo_desconto]').val('0');
        prod_formset.find('input[id$=-desconto]').val('0,00');
        prod_formset.find('input[id$=-subtotal]').val('0,00');
        prod_formset.find('input[id$=-total_sem_desconto]').val('0,00');
        prod_formset.find('input[id$=_frete]').val('0,00');
        prod_formset.find('input[id$=_despesas]').val('0,00');
        prod_formset.find('input[id$=_seguro]').val('0,00');
        prod_formset.find('input[id$=-total_impostos]').val('0,00');
        prod_formset.find('input[id$=-total_com_impostos]').val('0,00');
        prod_formset.find('input.modal-field[type=text]').val('0.00');

        prod_formset.find('input[id$=-auto_calcular_impostos]').prop('checked', true);

    },

    hideModalFields: function(prod_formset){
        //Esconder campos de impostos dos modais
        var hide_td = prod_formset.find('.modal-field').parent('.field-td');

        hide_td.each(function(){
            $(this).closest('table').find('th').eq($(this).index()).hide();
            $(this).hide();
        });

        //Adicionar icone de impostos
        prod_formset.find('input.modal-field[type=text]').each(function(){
            if(!$(this).val()){ $(this).val('0.00'); }
        });
        prod_formset.find('input[id$=calculo_imposto]').replaceWith($('<i class="material-icons imposto-icon">&#xE8B0;</i>'));
        prod_formset.find('.imposto-icon').parent('.field-td').css('min-width', '50px');
    },

    mostrarModalImposto: function(prod_formset){
        var form_numb = prod_formset.prop('id').match(/\d+/);
        var subtotal = prod_formset.find('input[id$=-subtotal]');
        var subtotal_s = prod_formset.find('input[id$=-total_sem_desconto]');
        var frete = prod_formset.find('input[id$=_frete]');
        var despesas = prod_formset.find('input[id$=_despesas]');
        var seguro = prod_formset.find('input[id$=_seguro]');

        $(".imposto_modal").modal('show').prop('id', form_numb);

        //Auto calcular impostos?
        $('#id_auto_calcular_modal').prop('checked', prod_formset.find('input[id$=-auto_calcular_impostos]').is(":checked")).change();

        //Rateio
        $('#id_rateio_desconto_modal').val(parseFloat(parseFloat(subtotal_s.val().replace(/\./g,'').replace(',','.')) - parseFloat(subtotal.val().replace(/\./g,'').replace(',','.'))).toFixed(2).replace(/\./g,','));
        $('#id_rateio_frete_modal').val(frete.val());
        $('#id_rateio_despesas_modal').val(despesas.val());
        $('#id_rateio_seguro_modal').val(seguro.val());

        //Cálculo
        $('#id_ipi_incluso_modal').prop('checked', prod_formset.find('input[id$=-ipi_incluido_preco]').is(":checked"));
        $('#id_icms_incluso_modal').prop('checked', prod_formset.find('input[id$=-icms_incluido_preco]').is(":checked"));
        $('#id_icmsst_incluso_modal').prop('checked', prod_formset.find('input[id$=-icmsst_incluido_preco]').is(":checked"));
        $('#id_ipi_bc_icms_modal').prop('checked', prod_formset.find('input[id$=-incluir_bc_icms]').is(":checked"));
        $('#id_ipi_bc_icmsst_modal').prop('checked', prod_formset.find('input[id$=-incluir_bc_icmsst]').is(":checked"));

        //Impostos
        $('#id_vbc_ipi_modal').val(prod_formset.find('input[id$=-vbc_ipi]').val().replace(/\./g,','));
        $('#id_pipi_modal').val(prod_formset.find('input[id$=-p_ipi]').val().replace(/\./g,','));
        $('#id_vipi_modal').val(prod_formset.find('input[id$=-vipi]').val().replace(/\./g,','));

        $('#id_vbc_icms_modal').val(prod_formset.find('input[id$=-vbc_icms]').val().replace(/\./g,','));
        $('#id_p_red_bc').val(prod_formset.find('input[id$=-p_red_bc]').val().replace(/\./g,','));
        $('#id_picms_modal').val(prod_formset.find('input[id$=-p_icms]').val().replace(/\./g,','));
        $('#id_vicms_modal').val(prod_formset.find('input[id$=-vicms]').val().replace(/\./g,','));

        $('#id_vbc_icmsst_modal').val(prod_formset.find('input[id$=-vbc_icms_st]').val().replace(/\./g,','));
        $('#id_pmvast_modal').val(prod_formset.find('input[id$=-p_mvast]').val().replace(/\./g,','));
        $('#id_p_red_bcst_modal').val(prod_formset.find('input[id$=-p_red_bcst]').val().replace(/\./g,','));
        $('#id_picmsst_modal').val(prod_formset.find('input[id$=-p_icmsst]').val().replace(/\./g,','));
        $('#id_vicmsst_modal').val(prod_formset.find('input[id$=-vicms_st]').val().replace(/\./g,','));

        $('#id_pfcp_modal').val(prod_formset.find('input[id$=-pfcp]').val().replace(/\./g,','));
        $('#id_picms_dest_modal').val(prod_formset.find('input[id$=-p_icms_dest]').val().replace(/\./g,','));
        $('#id_picms_inter_modal').val(prod_formset.find('input[id$=-p_icms_inter]').val().replace(/\./g,','));
        $('#id_picms_part_modal').val(prod_formset.find('input[id$=-p_icms_part]').val().replace(/\./g,','));
        $('#id_vfcp_modal').val(prod_formset.find('input[id$=-vfcp]').val().replace(/\./g,','));
        $('#id_vicms_remet_modal').val(prod_formset.find('input[id$=-vicmsufremet]').val().replace(/\./g,','));
        $('#id_vicms_dest_modal').val(prod_formset.find('input[id$=-vicmsufdest]').val().replace(/\./g,','));

        //Totais
        $('#id_total_impostos_modal').val(prod_formset.find('input[id$=-total_impostos]').val().replace(/\./g,','));
        $('#id_subtotal_modal').val(subtotal.val().replace(/\./g,','));
        $('#id_total_modal').val(prod_formset.find('input[id$=-total_com_impostos]').val().replace(/\./g,','));
    },

    formTableInit: function(){
        //caso haja erro no form de adicionar, precisa esconder essa linha novamente.
        $('#venda_form_add .pagamentos_table tbody tr:first-child,#compra_form_add .pagamentos_table tbody tr:first-child').addClass('hidden');

        //Esconder campos delete da tabela
        $('.formset-tr-field').each(function(){
            $.Admin.formset.hideDeleteField($(this));
        });

        //Esconder forms com delete checked
        $('.pagamentos_table tbody tr input[type=checkbox]:hidden:checked').each(function(){
            $(this).closest('tr').addClass('hidden');
        });
    },

    ratearValores: function(){
        var tipo_desconto_tot = $('#id_tipo_desconto').val();
        var desconto_total = $('#id_desconto');
        var vdesconto_total = parseFloat(parseFloat($(desconto_total).val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        var frete_total = $('#id_frete');
        var vfrete_total = parseFloat(parseFloat($(frete_total).val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        var despesas_totais = $('#id_despesas');
        var vdespesas_totais = parseFloat(parseFloat($(despesas_totais).val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        var seguro_total = $('#id_seguro');
        var vseguro_total = parseFloat(parseFloat($(seguro_total).val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        var total = $('#id_valor_total');
        var total_sem_adicionais = $('#id_valor_total').val().replace(/\./g,'').replace(',','.');

        //Desconto
        if(tipo_desconto_tot == '0' && !isNaN(vdesconto_total)){
            vdesconto_total = parseFloat(parseFloat($(desconto_total).val().replace(/\./g,'').replace(',','.'))).toFixed(2);
            total_sem_adicionais = parseFloat(parseFloat(total_sem_adicionais) + parseFloat(vdesconto_total)).toFixed(2);
        }else if(tipo_desconto_tot == '1' && !isNaN(vdesconto_total)){
            var vtot = parseFloat(total.val().replace(/\./g,'').replace(',','.')).toFixed(2);
            total_sem_adicionais = parseFloat(parseFloat(parseFloat(vtot)*100)/parseFloat(100-parseFloat(desconto_total.val().replace(/\./g,'').replace(',','.')))).toFixed(2);
            vdesconto_total = parseFloat(parseFloat(total_sem_adicionais) - parseFloat(vtot)).toFixed(2);
        }

        if(isNaN(vdesconto_total)) vdesconto_total = 0;
        if(isNaN(vfrete_total)) vfrete_total = 0;
        if(isNaN(vdespesas_totais)) vdespesas_totais = 0;
        if(isNaN(vseguro_total)) vseguro_total = 0;

        total_sem_adicionais = parseFloat(parseFloat(total_sem_adicionais) - parseFloat(vfrete_total)).toFixed(2);
        total_sem_adicionais = parseFloat(parseFloat(total_sem_adicionais) - parseFloat(vdespesas_totais)).toFixed(2);
        total_sem_adicionais = parseFloat(parseFloat(total_sem_adicionais) - parseFloat(vseguro_total)).toFixed(2);

        var produtos_form = $('.formset[id^=produtos_form-]:visible');
        var n_produtos = produtos_form.length;
        var desconto_atual = 0;
        var frete_atual = 0;
        var despeasas_atual = 0;
        var seguro_atual = 0;

        produtos_form.each(function(index){
            if($(this).find('select[id$=-produto]').val()){
                var vtotal_s = $(this).find('input[id$=-total_sem_desconto]').val().replace(/\./g,'').replace(',','.');
                var desconto_input = $(this).find('input[id$=-desconto]');
                var frete_input = $(this).find('input[id$=-valor_rateio_frete]');
                var despesas_input = $(this).find('input[id$=-valor_rateio_despesas]');
                var seguro_input = $(this).find('input[id$=-valor_rateio_seguro]');

                var frete_item = frete_input.val().replace(/\./g,'').replace(',','.');
                var despesas_item = despesas_input.val().replace(/\./g,'').replace(',','.');
                var seguro_item = seguro_input.val().replace(/\./g,'').replace(',','.');

                if(isNaN(vtotal_s)) vtotal_s = '0.00';
                if(isNaN(frete_item)) frete_item = '0.00';
                if(isNaN(despesas_item)) despesas_item = '0.00';
                if(isNaN(seguro_item)) seguro_item = '0.00';

                //Subtrair valores já preenchidos
                vtotal_s = parseFloat(vtotal_s) - parseFloat(frete_item) - parseFloat(despesas_item) - parseFloat(seguro_item);
                var percentual_do_total = 0;
                if(parseFloat(total_sem_adicionais) > 0){
                    var percentual_do_total = parseFloat(parseFloat(vtotal_s)/parseFloat(total_sem_adicionais)).toFixed(2);
                }

                var vdesconto_aplicado = parseFloat(percentual_do_total*vdesconto_total).toFixed(2);
                desconto_atual = parseFloat(desconto_atual) + parseFloat(vdesconto_aplicado);

                var vfrete_aplicado = parseFloat(percentual_do_total*vfrete_total).toFixed(2);
                frete_atual = parseFloat(frete_atual) + parseFloat(vfrete_aplicado);

                var vdespesas_aplicadas = parseFloat(percentual_do_total*vdespesas_totais).toFixed(2);
                despeasas_atual = parseFloat(despeasas_atual) + parseFloat(vdespesas_aplicadas);

                var vseguro_aplicado = parseFloat(percentual_do_total*vseguro_total).toFixed(2);
                seguro_atual = parseFloat(seguro_atual) + parseFloat(vseguro_aplicado);

                //Rateio desconto
                $(this).find('input[id$=-tipo_desconto]').val('0');
                desconto_input.val(vdesconto_aplicado.toString().replace(/\./g,','));

                frete_input.val(vfrete_aplicado.toString().replace(/\./g,','));
                despesas_input.val(vdespesas_aplicadas.toString().replace(/\./g,','));
                seguro_input.val(vseguro_aplicado.toString().replace(/\./g,','));

                if(index == n_produtos - 1){
                    var diferenca = 0;
                    if(desconto_atual != vdesconto_total){
                        diferenca = vdesconto_total - desconto_atual;
                        vdesconto_aplicado = parseFloat(parseFloat(vdesconto_aplicado) + parseFloat(diferenca)).toFixed(2);
                        desconto_input.val(vdesconto_aplicado.toString().replace(/\./g,','));
                    }

                    if(frete_atual != vfrete_total){
                        diferenca = vfrete_total - frete_atual;
                        vfrete_aplicado = parseFloat(parseFloat(vfrete_aplicado) + parseFloat(diferenca)).toFixed(2);
                        frete_input.val(vfrete_aplicado.toString().replace(/\./g,','));
                    }

                    if(despeasas_atual != vdespesas_totais){
                        diferenca = vdespesas_totais - despeasas_atual;
                        vdespesas_aplicadas = parseFloat(parseFloat(vdespesas_aplicadas) + parseFloat(diferenca)).toFixed(2);
                        despesas_input.val(vdespesas_aplicadas.toString().replace('.',','));
                    }

                    if(seguro_atual != vseguro_total){
                        diferenca = vseguro_total - seguro_atual;
                        vseguro_aplicado = parseFloat(parseFloat(vseguro_aplicado) + parseFloat(diferenca)).toFixed(2);
                        seguro_input.val(vseguro_aplicado.toString().replace('.',','));
                    }

                    desconto_input.change();
                }
            }
        });
    },

    setItensFields: function(form_number){
        var form_atual = $('div[id=produtos_form-' + form_number + ']');
        var val_unit = form_atual.find('input[id$=-valor_unit]');
        var qtd = form_atual.find('input[id$=-quantidade]');
        var tipo_desconto = form_atual.find('select[id$=-tipo_desconto]');
        var desconto = form_atual.find('input[id$=-desconto]');
        var frete = form_atual.find('input[id$=-valor_rateio_frete]');
        var despesas = form_atual.find('input[id$=-valor_rateio_despesas]');
        var seguro = form_atual.find('input[id$=-valor_rateio_seguro]');
        var subtotal = form_atual.find('input[id$=-subtotal]');
        var total_sem_desconto = form_atual.find('input[id$=-total_sem_desconto]');
        var total = form_atual.find('input[id$=-total_com_impostos]');
        var total_impostos = form_atual.find('input[id$=-total_impostos]');
        var vprod = parseFloat(parseFloat(qtd.val().replace(/\./g,'').replace(',','.'))*parseFloat(val_unit.val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        var vtotal = vprod;
        var vtotal_impostos = 0;
        var vsubtotal_sem_desconto = 0;
        var vtotal_sem_impostos = 0;

        var vdesconto = parseFloat($(desconto).val().replace(/\./g,'').replace(',','.'));
        var vfrete = parseFloat(frete.val().replace(/\./g,'').replace(',','.'));
        var vdespesas = parseFloat(despesas.val().replace(/\./g,'').replace(',','.'));
        var vseguro = parseFloat(seguro.val().replace(/\./g,'').replace(',','.'));

        if(tipo_desconto.val() == '0' && !isNaN(vdesconto)){
            vtotal = parseFloat(parseFloat(vtotal) - parseFloat(vdesconto)).toFixed(2);
        }else if(tipo_desconto.val() == '1' && !isNaN(vdesconto)){
            vdesconto = parseFloat((parseFloat(vdesconto)/100)*parseFloat(vtotal).toFixed(2)).toFixed(2);
            vtotal = parseFloat(parseFloat(vtotal) - parseFloat(vdesconto)).toFixed(2);
        }

        if(!isNaN(vtotal)){
            if(!isNaN(vfrete)){
                vtotal = parseFloat(vtotal) + parseFloat(vfrete);
            }
            if(!isNaN(vdespesas)){
                vtotal = parseFloat(vtotal) + parseFloat(vdespesas);
            }
            if(!isNaN(vseguro)){
                vtotal = parseFloat(vtotal) + parseFloat(vseguro);
            }
            vsubtotal_sem_desconto = parseFloat(vtotal) + parseFloat(vdesconto);
            vtotal_sem_impostos = parseFloat(vtotal);
        }

        /*   Impostos   */
        if(form_atual.find('select[id$=-produto]').val() && form_atual.find('input[id$=-auto_calcular_impostos]').is(':checked')){
            var pipi = form_atual.find('input[id$=-p_ipi]').val();
            var picms = form_atual.find('input[id$=-p_icms]').val();
            var picmsst = form_atual.find('input[id$=-p_icmsst]').val();
            var pfcp = form_atual.find('input[id$=-pfcp]').val();
            var picmsdest = form_atual.find('input[id$=-p_icms_dest]').val();
            var picmsinter = form_atual.find('input[id$=-p_icms_inter]').val();
            var picmspart = form_atual.find('input[id$=-p_icms_part]').val();
            var vipi = 0;
            var vicms = 0;
            var vicmsst = 0;
            var vfcp = 0;
            var vicmsdest = 0;
            var vicmsremet = 0;
            var red_bc_icms = parseFloat(parseFloat(form_atual.find('input[id$=-p_red_bc]').val())/100);
            var red_bc_icmsst = parseFloat(parseFloat(form_atual.find('input[id$=-p_red_bcst]').val())/100);
            var tipo_ipi = form_atual.find('select[id$=-tipo_ipi]').val();
            var ipi_bc_icms = form_atual.find('input[id$=-incluir_bc_icms]').is(':checked');
            var ipi_bc_icmsst = form_atual.find('input[id$=-incluir_bc_icmsst]').is(':checked');
            var pmvast = parseFloat(parseFloat(form_atual.find('input[id$=-p_mvast]').val())/100);

            //Calculo IPI
            if(tipo_ipi == '0'){
                form_atual.find('input[id$=-vipi]').val('0.00');
            }else if(tipo_ipi == '1'){
                vfixo_ipi = form_atual.find('input[id$=-vfixo_ipi]').val().replace(',','.');
                vipi = parseFloat(parseFloat(vfixo_ipi)*parseFloat(qtd.val().replace(/\./g,'').replace(',','.')));
                form_atual.find('input[id$=-vipi]').val(parseFloat(vipi).toFixed(2));
                if(form_atual.find('input[id$=-ipi_incluido_preco]').is(':checked')){
                    vtotal_sem_impostos = parseFloat(vtotal_sem_impostos) - parseFloat(vipi);
                }
            }else if(tipo_ipi == '2'){
                if(form_atual.find('input[id$=-ipi_incluido_preco]').is(':checked')){
                    vipi = parseFloat(parseFloat(vprod)*parseFloat(pipi)/(100+parseFloat(pipi))).toFixed(2);
                    form_atual.find('input[id$=-vipi]').val(parseFloat(vipi).toFixed(2));
                    vtotal_sem_impostos = parseFloat(vtotal_sem_impostos) - parseFloat(vipi);
                }else{
                    vipi = parseFloat(parseFloat(vsubtotal_sem_desconto)*parseFloat(pipi)/100).toFixed(2);
                    form_atual.find('input[id$=-vbc_ipi]').val(parseFloat(vsubtotal_sem_desconto).toFixed(2));
                    form_atual.find('input[id$=-vipi]').val(parseFloat(vipi).toFixed(2));
                }
            }
            vtotal_impostos = parseFloat(vtotal_impostos) + parseFloat(vipi);

            //Calculo ICMS
            if(parseFloat(picms) > 0){
                if(form_atual.find('input[id$=-icms_incluido_preco]').is(':checked')){
                    vicms = parseFloat(parseFloat(vprod)*parseFloat(picms)/(100+parseFloat(picms))).toFixed(2);
                    form_atual.find('input[id$=-vicms]').val(parseFloat(vicms).toFixed(2));
                    vtotal_sem_impostos = parseFloat(vtotal_sem_impostos) - parseFloat(vicms);
                }else if(ipi_bc_icms){
                    var vbc_icms = parseFloat(vtotal) + parseFloat(vipi);
                    vbc_icms = parseFloat(vbc_icms) - parseFloat(vbc_icms)*parseFloat(red_bc_icms);
                    vicms = parseFloat(parseFloat(vbc_icms)*parseFloat(picms)/100).toFixed(2);
                    form_atual.find('input[id$=-vbc_icms]').val(parseFloat(vbc_icms).toFixed(2));
                    form_atual.find('input[id$=-vicms]').val(parseFloat(vicms).toFixed(2));
                }else{
                    var vbc_icms = parseFloat(vtotal);
                    vbc_icms = parseFloat(vbc_icms) - parseFloat(vbc_icms)*parseFloat(red_bc_icms);
                    vicms = parseFloat(parseFloat(vbc_icms)*parseFloat(picms)/100).toFixed(2);
                    form_atual.find('input[id$=-vbc_icms]').val(parseFloat(vbc_icms).toFixed(2));
                    form_atual.find('input[id$=-vicms]').val(parseFloat(vicms).toFixed(2));
                }
            }
            vtotal_impostos = parseFloat(vtotal_impostos) + parseFloat(vicms);

            //Calculo ICMS-ST
            if(parseFloat(picmsst) > 0){
                if(form_atual.find('input[id$=-icmsst_incluido_preco]').is(':checked')){
                    vicmsst = parseFloat(parseFloat(vprod)*parseFloat(picmsst)/(100+parseFloat(picmsst))).toFixed(2);
                    form_atual.find('input[id$=-vicms_st]').val(parseFloat(vicmsst).toFixed(2));
                    vtotal_sem_impostos = parseFloat(vtotal_sem_impostos) - parseFloat(vicmsst);
                }else if(ipi_bc_icmsst){
                    var vbc_icms_inter = parseFloat(vtotal);
                    var vicms_inter = parseFloat(vbc_icms_inter)*parseFloat(picms)/100;
                    var vbc_icms_st = parseFloat(parseFloat(parseFloat(vtotal) + parseFloat(vipi))*(1 + parseFloat(pmvast)));
                    vbc_icms_st = parseFloat(vbc_icms_st) - parseFloat(vbc_icms_st)*parseFloat(red_bc_icmsst);
                    vicmsst = parseFloat(parseFloat(parseFloat(vbc_icms_st)*parseFloat(picmsst)/100) - parseFloat(vicms_inter)).toFixed(2);
                    form_atual.find('input[id$=-vbc_icms_st]').val(parseFloat(vbc_icms_st).toFixed(2));
                    form_atual.find('input[id$=-vicms_st]').val(parseFloat(vicmsst).toFixed(2));
                }else{
                    var vbc_icms_inter = parseFloat(vtotal);
                    var vicms_inter = parseFloat(vbc_icms_inter)*parseFloat(picms)/100;
                    var vbc_icms_st = parseFloat(parseFloat(vtotal)*(1 + parseFloat(pmvast)));
                    vbc_icms_st = parseFloat(vbc_icms_st) - parseFloat(vbc_icms_st)*parseFloat(red_bc_icmsst);
                    vicmsst = parseFloat((parseFloat(vbc_icms_st)*parseFloat(picmsst)/100) - parseFloat(vicms_inter)).toFixed(2);
                    form_atual.find('input[id$=-vbc_icms_st]').val(parseFloat(vbc_icms_st).toFixed(2));
                    form_atual.find('input[id$=-vicms_st]').val(parseFloat(vicmsst).toFixed(2));
                }
            }
            vtotal_impostos = parseFloat(vtotal_impostos) + parseFloat(vicmsst);

            //Calculo ICMS Partilha
            if(parseFloat(pfcp) > 0 || parseFloat(picmsdest) > 0 || parseFloat(picmsinter)){
                var vbcicmspart = parseFloat(vtotal) + parseFloat(vipi);
                vfcp = parseFloat(pfcp)*parseFloat(vbcicmspart)/100;
                var vdifal = parseFloat(parseFloat(vbcicmspart)*(parseFloat(picmsdest)-parseFloat(picmsinter))/100).toFixed(2);
                vicmsdest = parseFloat(parseFloat(vdifal)*parseFloat(picmspart)/100).toFixed(2);
                vicmsremet = parseFloat(parseFloat(vdifal)*(100 - parseFloat(picmspart))/100).toFixed(2);
                form_atual.find('input[id$=-vfcp]').val(parseFloat(vfcp).toFixed(2));
                form_atual.find('input[id$=-vicmsufdest]').val(parseFloat(vicmsdest).toFixed(2));
                form_atual.find('input[id$=-vicmsufremet]').val(parseFloat(vicmsremet).toFixed(2));
            }
            vtotal_impostos = parseFloat(vtotal_impostos) + parseFloat(vfcp) + parseFloat(vicmsdest) + parseFloat(vicmsremet);

            vsubtotal_sem_desconto = parseFloat(vtotal_sem_impostos) + parseFloat(vdesconto);
            vtotal = parseFloat(vtotal_sem_impostos) + parseFloat(vtotal_impostos);

        }else{
            //Caso totais ja foram preenchidos pelo usuario
            var vipi = form_atual.find('input[id$=-vipi]').val().replace(/\./g,'').replace(',','.');
            var vicms = form_atual.find('input[id$=-vicms]').val().replace(/\./g,'').replace(',','.');
            var vicmsst = form_atual.find('input[id$=-vicms_st]').val().replace(/\./g,'').replace(',','.');
            vtotal_impostos = parseFloat(vipi) + parseFloat(vicms) + parseFloat(vicmsst);

            if(form_atual.find('input[id$=-ipi_incluido_preco]').is(':checked')){
                vtotal_sem_impostos = parseFloat(vtotal_sem_impostos) - parseFloat(vipi);
            }
            if(form_atual.find('input[id$=-icms_incluido_preco]').is(':checked')){
                vtotal_sem_impostos = parseFloat(vtotal_sem_impostos) - parseFloat(vicms);
            }
            if(form_atual.find('input[id$=-icmsst_incluido_preco]').is(':checked')){
                vtotal_sem_impostos = parseFloat(vtotal_sem_impostos) - parseFloat(vicmsst);
            }

            vsubtotal_sem_desconto = parseFloat(vtotal_sem_impostos) + parseFloat(vdesconto);
            vtotal = parseFloat(vtotal_sem_impostos) + parseFloat(vtotal_impostos);

        }

        //Totais
        total_impostos.val(parseFloat(vtotal_impostos).toFixed(2).replace('.',','));
        total_sem_desconto.val(parseFloat(vsubtotal_sem_desconto).toFixed(2).replace('.',','))
        subtotal.val(parseFloat(vtotal_sem_impostos).toFixed(2).replace('.',','));
        total.val(parseFloat(vtotal).toFixed(2).replace('.',','));

        subtotal.change();
    },

    setAdicionaisTotal: function(){
        var tipo_desconto_tot = $('#id_tipo_desconto').val();
        var desconto_total = $('#id_desconto');
        var vdesconto_total = 0;
        var frete_total = $('#id_frete');
        var vfrete_total = 0;
        var despesas_totais = $('#id_despesas');
        var vdespesas_totais = 0;
        var seguro_total = $('#id_seguro');
        var vseguro_total = 0;
        var imposto_total = $('#id_impostos');
        var vimposto_total = 0;
        var vtotal_sem_desconto = 0;

        $('.formset[id^=produtos_form-]:visible').each(function(){
            var tipo_desconto = $(this).find('select[id$=-tipo_desconto]').eq(0).val()
            var desconto = $(this).find('input[id$=-desconto]').eq(0);
            var vdesconto = 0;
            var vfrete_item = $(this).find('input[id$=_frete]').eq(0).val();
            var vdespesas_item = $(this).find('input[id$=_despesas]').eq(0).val();
            var vseguro_item = $(this).find('input[id$=_seguro]').eq(0).val();
            var vimpostos_item = $(this).find('input[id$=-total_impostos]').eq(0).val();
            var vsubtotal_sem_desconto = $(this).find('input[id$=-total_sem_desconto]').eq(0).val().replace(/\./g,'').replace(',','.');

            if(!isNaN(parseFloat(vfrete_item))){
                vfrete_total = parseFloat(vfrete_total) + parseFloat(vfrete_item.replace(/\./g,'').replace(',','.'));
                vsubtotal_sem_desconto = parseFloat(vsubtotal_sem_desconto) - parseFloat(vfrete_item.replace(/\./g,'').replace(',','.'));
            }
            if(!isNaN(parseFloat(vdespesas_item))){
                vdespesas_totais = parseFloat(vdespesas_totais) + parseFloat(vdespesas_item.replace(/\./g,'').replace(',','.'));
                vsubtotal_sem_desconto = parseFloat(vsubtotal_sem_desconto) - parseFloat(vdespesas_item.replace(/\./g,'').replace(',','.'));
            }
            if(!isNaN(parseFloat(vseguro_item))){
                vseguro_total = parseFloat(vseguro_total) + parseFloat(vseguro_item.replace(/\./g,'').replace(',','.'));
                vsubtotal_sem_desconto = parseFloat(vsubtotal_sem_desconto) - parseFloat(vseguro_item.replace(/\./g,'').replace(',','.'));
            }
            if(!isNaN(parseFloat(vimpostos_item))){
                vimposto_total = parseFloat(vimposto_total) + parseFloat(vimpostos_item.replace(/\./g,'').replace(',','.'));
            }

            if(tipo_desconto == '0'){
                vdesconto = parseFloat(parseFloat($(desconto).val().replace(/\./g,'').replace(',','.'))).toFixed(2);
            }else if(tipo_desconto == '1'){
                vdesconto = (parseFloat($(desconto).val().replace(/\./g,'').replace(',','.'))/100)*parseFloat(vsubtotal_sem_desconto);
            }

            if(!isNaN(vdesconto)){
                vdesconto_total = parseFloat(vdesconto_total) + parseFloat(vdesconto);
            }

            vtotal_sem_desconto = parseFloat(vtotal_sem_desconto) + parseFloat(vsubtotal_sem_desconto);

        });

        vdesconto_total = parseFloat(vdesconto_total);

        if(tipo_desconto_tot == '0' && !isNaN(vdesconto_total)){
            desconto_total.val(parseFloat(vdesconto_total).toFixed(2).replace(/\./g,','));
        }else if(tipo_desconto_tot == '1' && !isNaN(vdesconto_total)){
            var pdesconto_total = parseFloat((parseFloat(vdesconto_total)*100)/parseFloat(vtotal_sem_desconto)).toFixed(4);

            if(!isNaN(pdesconto_total)){
                desconto_total.val(pdesconto_total.replace('.',','));
            }
        }

        if(!isNaN(vfrete_total)){
            frete_total.val(parseFloat(vfrete_total).toFixed(2).replace(/\./g,','));
        }
        if(!isNaN(vdespesas_totais)){
            despesas_totais.val(parseFloat(vdespesas_totais).toFixed(2).replace(/\./g,','));
        }
        if(!isNaN(vseguro_total)){
            seguro_total.val(parseFloat(vseguro_total).toFixed(2).replace(/\./g,','));
        }
        if(!isNaN(vimposto_total)){
            imposto_total.val(parseFloat(vimposto_total).toFixed(2).replace(/\./g,','));
        }

    },

    setTotalFields: function(){
        var tipo_desconto = $('#id_tipo_desconto');
        var desconto = $('#id_desconto');
        var vtotal = 0;
        var vtotal_sem_imposto = 0;
        var adicionais = 0;

        $('input[id$=-total_sem_desconto]:visible').each(function(){
            var vtotal_sem_desconto = parseFloat($(this).val().replace(/\./g,'').replace(',','.')).toFixed(2);
            if(!isNaN(vtotal_sem_desconto)){
                vtotal = parseFloat(parseFloat(vtotal) + parseFloat(vtotal_sem_desconto)).toFixed(2);
            }
        });

        //Subtrair adicionais (frete, despesas e seguro), do valor total, para não somar duas vezes
        $('input[id$=-valor_rateio_frete]:visible,input[id$=-valor_rateio_despesas]:visible,input[id$=-valor_rateio_seguro]:visible').each(function(){
            var vrateio = parseFloat($(this).val().replace(/\./g,'').replace(',','.')).toFixed(2);
            if(!isNaN(vrateio)){
                adicionais = parseFloat(parseFloat(adicionais) + parseFloat(vrateio)).toFixed(2);
            }
        });

        if(tipo_desconto.val() == '0'){
            vtotal = parseFloat(parseFloat(vtotal) - parseFloat($(desconto).val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        }else if(tipo_desconto.val() == '1'){
            vtotal = parseFloat(parseFloat(vtotal) - (parseFloat($(desconto).val().replace(/\./g,'').replace(',','.'))/100)*parseFloat(vtotal)).toFixed(2);
        }

        if(!isNaN(adicionais) && !isNaN(vtotal)){
            vtotal = parseFloat(vtotal) - parseFloat(adicionais);
        }

        vtotal = parseFloat(parseFloat(vtotal) + parseFloat($('#id_frete').val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        vtotal = parseFloat(parseFloat(vtotal) + parseFloat($('#id_despesas').val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        vtotal = parseFloat(parseFloat(vtotal) + parseFloat($('#id_seguro').val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        vtotal_sem_imposto = parseFloat(vtotal);
        vtotal = parseFloat(parseFloat(vtotal) + parseFloat($('#id_impostos').val().replace(/\./g,'').replace(',','.'))).toFixed(2);

        if(!isNaN(vtotal)){
            $('#id_total_sem_imposto').val(vtotal_sem_imposto.toString().replace(/\./g,','));
            $('#id_valor_total').val(vtotal.replace(/\./g,','));
            $('#id_valor_total_display').text(vtotal.replace(/\./g,','));
        }
    },

    alterarFieldsModal: function(auto_calcular){
        //Caso usuario remova o calculo automatico
        if(!auto_calcular){
            $('.imposto_modal').find('.campo_imposto_editavel').each(function(){
                $(this).prop('readonly', false);
                $(this).removeClass('input_no_edit');
            });
        }else{
            $('.imposto_modal').find('.campo_imposto_editavel').each(function(){
                $(this).prop('readonly', true);
                $(this).addClass('input_no_edit');
            });
        }
    },

    salvarInfoImpostoModal: function(modal){
        var form_atual = $('#produtos_form-' + modal.prop('id'));

        form_atual.find('input[id$=-auto_calcular_impostos]').prop('checked', modal.find('#id_auto_calcular_modal').is(':checked'));

        //Rateio
        form_atual.find('input[id$=-desconto]').val(modal.find('#id_rateio_desconto_modal').val());
        form_atual.find('input[id$=-valor_rateio_frete]').val(modal.find('#id_rateio_frete_modal').val());
        form_atual.find('input[id$=-valor_rateio_despesas]').val(modal.find('#id_rateio_despesas_modal').val());
        form_atual.find('input[id$=-valor_rateio_seguro]').val(modal.find('#id_rateio_seguro_modal').val());

        //Opcoes
        form_atual.find('input[id$=-ipi_incluido_preco]').prop('checked', modal.find('#id_ipi_incluso_modal').is(':checked'));
        form_atual.find('input[id$=-icms_incluido_preco]').prop('checked', modal.find('#id_icms_incluso_modal').is(':checked'));
        form_atual.find('input[id$=-icmsst_incluido_preco]').prop('checked', modal.find('#id_icmsst_incluso_modal').is(':checked'));
        form_atual.find('input[id$=-incluir_bc_icms]').prop('checked', modal.find('#id_ipi_bc_icms_modal').is(':checked'));
        form_atual.find('input[id$=-incluir_bc_icmsst]').prop('checked', modal.find('#id_ipi_bc_icmsst_modal').is(':checked'));

        //IPI
        form_atual.find('input[id$=-vbc_ipi]').val(modal.find('#id_vbc_ipi_modal').val());
        form_atual.find('input[id$=-p_ipi]').val(modal.find('#id_pipi_modal').val());
        form_atual.find('input[id$=-vipi]').val(modal.find('#id_vipi_modal').val());

        //ICMS
        form_atual.find('input[id$=-vbc_icms]').val(modal.find('#id_vbc_icms_modal').val());
        form_atual.find('input[id$=-p_icms]').val(modal.find('#id_picms_modal').val());
        form_atual.find('input[id$=-vicms]').val(modal.find('#id_vicms_modal').val());

        //ICMS-ST
        form_atual.find('input[id$=-vbc_icms_st]').val(modal.find('#id_vbc_icmsst_modal').val());
        form_atual.find('input[id$=-p_icmsst]').val(modal.find('#id_picmsst_modal').val());
        form_atual.find('input[id$=-vicms_st]').val(modal.find('#id_vicmsst_modal').val());

        //ICMS Partilha
        form_atual.find('input[id$=-vfcp]').val(modal.find('#id_vfcp_modal').val());
        form_atual.find('input[id$=-vicmsufremet]').val(modal.find('#id_vicms_remet_modal').val());
        form_atual.find('input[id$=-vicmsufdest]').val(modal.find('#id_vicms_dest_modal').val());

        form_atual.find('select[id$=-tipo_desconto]').val('0').trigger('change');
    },

    setTotalParcelasFields: function(){
        var total = parseFloat($('#id_valor_total_display').text().replace(/\./g,'').replace(',','.'));
        var parcelas_inputs = $('tr:not(.hidden) input[id$=-valor_parcela]');
        if(parcelas_inputs.length){
            var valores_parcelas = [];
            var total_atual = 0;

            for (i = 0; i < parcelas_inputs.length; i++){
                var resto = total - total_atual;
                var parcela_atual = resto > 0 ? Math.max(parseFloat(resto / (parcelas_inputs.length - i)).toFixed(2), 0.01) : 0;
                if(valores_parcelas.length && valores_parcelas[valores_parcelas.length - 1] >= parcela_atual){
                    valores_parcelas.push(parcela_atual);
                }else{
                    valores_parcelas.unshift(parcela_atual);
                }
                total_atual += parcela_atual;
            }

            i = 0;
            parcelas_inputs.each(function(){
                $(this).val(parseFloat(valores_parcelas[i]).toFixed(2).replace(/\./g,','));
                i++;
            });
        }
    },

    verificarParcelas: function(){
        var _this = this;
        var total_display_icon = $('.total-display i');
        var produtos_tab = $('#tab_produtos');
        var valid = true;

        total_display_icon.addClass('hidden');

        if(!_this.checkSomaParcelas()){
            $('a[href="#tab_pagamento"]').tab('show');
            total_display_icon.removeClass('hidden');
            valid = false;
        }

        produtos_tab.find('select[id$=-produto]').each(function(){
            if(!$(this).val() && !($(this).parents('.formset').css('display') == 'none')){
                $('a[href="#tab_produtos"]').tab('show');
                $(this).css('border-color', 'red')
                valid = false;
            }
        });
        return valid;
    },

    checkSomaParcelas: function(){
        var soma_parcelas = 0;
        var valor_total = $('#id_valor_total_display').text().replace(/\./g,'').replace(',','.');

        $('.pagamentos_table tbody tr:not(.hidden) input[id$=-valor_parcela]').each(function(){
            var parcela = parseFloat($(this).val().replace(/\./g,'').replace(',','.'))
            if(parcela && !isNaN(parcela)){
                soma_parcelas += parseFloat(parcela);
            }
        });

        if(parseFloat(soma_parcelas).toFixed(2) === parseFloat(valor_total).toFixed(2)){
            return true;
        }else{
            return false;
        }
    },

    handlePagamentoInfo: function(data, initial){
        var n_parcelas_input = $('#id_n_parcelas');

        if(typeof data === 'undefined' || !data){
            n_parcelas_input.text('');
        }else{
            n_parcelas_input.text(data[0].fields.n_parcelas);
        }

        if(!initial){
            $.Admin.formset.createNewTrForms($('.pagamentos_table'), n_parcelas_input.text());
            $.Admin.datepicker.init();

            if(data){
                //Preencher indice das parcelas automaticamente
                var ind_parcela = 1;
                $('input[id$=-indice_parcela]:visible').each(function(){
                    $(this).val(ind_parcela);
                    ind_parcela++;
                });

                //Preencher datas de vencimento  das parcelas automaticamente
                var dias_prazo_atual = data[0].fields.parcela_inicial;
                $('input[id$=-vencimento]:visible').first().val($.Admin.datepicker.addDaysToDate(data[0].fields.parcela_inicial));

                $('input[id$=-vencimento]:not(:first)').each(function(){
                    dias_prazo_atual = dias_prazo_atual + data[0].fields.dias_recorrencia;
                    $(this).val($.Admin.datepicker.addDaysToDate(dias_prazo_atual));
                });
            }
        }

    },

    handleProdutoInfo: function(data, form_number, initial){
        var val_unit = $('#id_produtos_form-'+ form_number + '-valor_unit');
        var form_atual = $('div[id=produtos_form-' +form_number+ ']');

        if(!initial){
            form_atual.find('input[type=text]').val('0');
            form_atual.find('input[id$=-quantidade]').val(1);
            form_atual.find('input[type=checkbox]').not('input[id$=-auto_calcular_impostos]').prop('checked',false);
        }

        if(typeof data === 'undefined' || !data){
            return;
        }else{
            if(data[0].fields.venda && !initial) val_unit.val(data[0].fields.venda.replace(/\./g,','));
            for(var i = 0; i < data.length; i++) {
                if(data[i].model == 'fiscal.icms' || data[i].model == 'fiscal.icmssn'){
                    if(data[i].fields.p_icms && !initial) form_atual.find('input[id$=-p_icms]').val(data[i].fields.p_icms);
                    if(data[i].fields.p_red_bc) form_atual.find('input[id$=-p_red_bc]').val(data[i].fields.p_red_bc);
                    if(data[i].fields.p_icmsst && !initial) form_atual.find('input[id$=-p_icmsst]').val(data[i].fields.p_icmsst);
                    if(data[i].fields.p_red_bcst) form_atual.find('input[id$=-p_red_bcst]').val(data[i].fields.p_red_bcst);
                    if(data[i].fields.p_mvast) form_atual.find('input[id$=-p_mvast]').val(data[i].fields.p_mvast);
                }

                if(data[i].model == 'fiscal.icms' && !initial){
                    form_atual.find('input[id$=-icms_incluido_preco]').prop('checked', data[i].fields.icms_incluido_preco);
                    form_atual.find('input[id$=-icmsst_incluido_preco]').prop('checked', data[i].fields.icmsst_incluido_preco);

                }else if(data[i].model == 'fiscal.icmssn' && !initial){
                    form_atual.find('input[id$=-icms_incluido_preco]').prop('checked', data[i].fields.icmssn_incluido_preco);
                    form_atual.find('input[id$=-icmsst_incluido_preco]').prop('checked', data[i].fields.icmssnst_incluido_preco);

                }else if(data[i].model == 'fiscal.ipi'){
                    if(!initial) form_atual.find('input[id$=-ipi_incluido_preco]').prop('checked', data[i].fields.ipi_incluido_preco);
                    if(!initial) form_atual.find('input[id$=-incluir_bc_icms]').prop('checked', data[i].fields.incluir_bc_icms);
                    if(!initial) form_atual.find('input[id$=-incluir_bc_icmsst]').prop('checked', data[i].fields.incluir_bc_icmsst);

                    form_atual.find('select[id$=-tipo_ipi]').val(data[i].fields.tipo_ipi);

                    if(data[i].fields.tipo_ipi == '0'  && !initial){
                        form_atual.find('input[id$=-p_ipi]').val('0.00');
                    }else if(data[i].fields.tipo_ipi == '1'  && !initial){
                        if(data[i].fields.valor_fixo) form_atual.find('input[id$=-vfixo_ipi]').val(data[i].fields.valor_fixo);
                    }else if(data[i].fields.tipo_ipi == '2'  && !initial){
                        if(data[i].fields.p_ipi) form_atual.find('input[id$=-p_ipi]').val(data[i].fields.p_ipi);
                    }
                }else if(data[i].model == 'fiscal.icmsufdest'){
                    if(data[i].fields.p_fcp_dest) form_atual.find('input[id$=-pfcp]').val(data[i].fields.p_fcp_dest);
                    if(data[i].fields.p_icms_dest) form_atual.find('input[id$=-p_icms_dest]').val(data[i].fields.p_icms_dest);
                    if(data[i].fields.p_icms_inter) form_atual.find('input[id$=-p_icms_inter]').val(data[i].fields.p_icms_inter);
                    if(data[i].fields.p_icms_inter_part) form_atual.find('input[id$=-p_icms_part]').val(data[i].fields.p_icms_inter_part);
                }

            }
            //Para trigger o metodo setItensFields
            if(!initial) form_atual.find('input[id$=-quantidade]').change();
        }
    },

    handleClienteInfo: function(data){
        if(typeof data === 'undefined' || !data){
            $('.display-cliente-field').text('');
        }else{
            $('.display-cliente-field').text('');
            for(var i = 0; i < data.length; i++) {
                if(data[i].model == 'cadastro.pessoajuridica'){
                    $('#cpf_cnpj_cliente').text(data[i].fields.cnpj);
                    $('#ie_rg_cliente').text(data[i].fields.inscricao_estadual);
                    $('#representante_cliente').text(data[i].fields.responsavel)
                }else if(data[i].model == 'cadastro.pessoafisica'){
                    $('#cpf_cnpj_cliente').text(data[i].fields.cpf);
                    $('#ie_rg_cliente').text(data[i].fields.rg);
                }

                if(data[i].model == 'cadastro.cliente'){
                    $('#limite_credito_cliente').text(data[i].fields.limite_de_credito.replace(/\./g,','));
                    var ind_ie = data[i].fields.indicador_ie;
                    if(ind_ie == '1'){
                        $('#ind_ie_cliente').text('Contribuinte ICMS');
                    }else if(ind_ie == '2'){
                        $('#ind_ie_cliente').text('Contribuinte isento de Inscrição');
                    }else if(ind_ie == '9'){
                        $('#ind_ie_cliente').text('Não Contribuinte');
                    }
                }

                if(data[i].model == 'cadastro.endereco'){
                    $('#endereco_cliente').text(data[i].fields.logradouro + ' ' + data[i].fields.numero);
                    $('#bairro_cliente').text(data[i].fields.bairro);
                    $('#municipio_cliente').text(data[i].fields.municipio);
                    $('#uf_cliente').text(data[i].fields.uf);
                    $('#cep_cliente').text(data[i].fields.cep);
                }

                if(data[i].model == 'cadastro.email'){
                    $('#email_cliente').text(data[i].fields.email);
                }

                if(data[i].model == 'cadastro.telefone'){
                    $('#telefone_cliente').text(data[i].fields.telefone);
                }
            }
        }
    },

    handleTransportadoraInfo: function(data){
        var veiculo_input = $('#id_veiculo');
        if(typeof data === 'undefined' || !data){
            veiculo_input.empty();
        }else{
            var valor_atual = veiculo_input.val();
            veiculo_input.empty();
            for(var i = 0; i < data.length; i++) {
                veiculo_input.append($('<option></option>').prop("value",data[i].pk).text(data[i].fields.descricao));
            }
            if(valor_atual){
                veiculo_input.val(valor_atual);
            }
        }
    },
}

$.Admin.compraForm = {
    init: function(req_urls) {
        var _this = this;
        var for_input = $('#id_fornecedor');
        var cond_pag_input = $('#id_cond_pagamento');
        var produtos_input = $('select.select-produto');

        $.Admin.maskInput.maskVenda();
        //Preencher campos edit view
        $('#id_valor_total_display').text($('#id_valor_total').val());

        $('.formset[id^=produtos_form-]').each(function(){
            var form_number = $(this).prop('id').match(/\d/)[0];
            if($(this).find('select[id$=-produto]').val().length === 0){
                $.Admin.vendaForm.setInitialItensData($(this));
            }
            $.Admin.vendaForm.hideModalFields($(this));
            if($('#compra_form_add').length) _this.setItensFields(form_number);
        });

        $.Admin.vendaForm.formTableInit();
        $.Admin.vendaForm.alterarFieldsModal(true);

        for_input.on('change', function(){
            if($(this).val()){
                var postData = {
                    'pessoaId': $(this).val(),
                }
                $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_fornecedor_url'], postData, _this.handleFornecedorInfo);
            }else{
                _this.handleFornecedorInfo();
            }
        });

        for_input.change();

        cond_pag_input.on('change', function(event, initial){
            if($(this).val()){
                var postData = {
                    'pagamentoId': $(this).val(),
                }
                $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_pagamento_url'], postData, $.Admin.vendaForm.handlePagamentoInfo, initial);
            }else{
                $.Admin.vendaForm.handlePagamentoInfo(null, initial);
            }
        });

        cond_pag_input.trigger('change', [true]);

        produtos_input.on('change', function(event, initial){
            var form_number = $(this).prop('id').match(/\d/)[0];
            if($(this).val()){
                var postData = {
                    'produtoId': $(this).val(),
                }
                $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_produto_url'], postData, _this.handleProdutoInfo, form_number, initial);
            }else{
                _this.handleProdutoInfo(null, form_number, initial);
            }
        });

        produtos_input.trigger('change', [true]);

        /*  Eventos  */

        //Caso campo esteja vazio manter 0
        $(document).on('change keyup', 'input[id$=-quantidade],input[id$=-valor_unit],input[id$=desconto],input[id$=frete],input[id$=despesas],input[id$=seguro],.imposto_modal .decimal-mask,.imposto_modal .decimal-mask-no-dot', function(){
            if(!$(this).val()) $(this).val('0');
        });

        //Atualiza valor total por item e adicionais totais
        $(document).on('load change keyup paste', 'input[id$=-quantidade],input[id$=-valor_unit],select[id$=-tipo_desconto],input[id$=-desconto]', function(){
            var form_number = $(this).prop('id').match(/\d/)[0];
            _this.setItensFields(form_number);
            _this.setAdicionaisTotal();
            $('#id_desconto').change();
        });

        //Atualiza o desconto total ao trocar o tipo de desconto
        $(document).on('change', '#id_tipo_desconto', function(){
            _this.setAdicionaisTotal();
        });

        //Atualiza o valor total da venda ao modificar o total dos itens, ou qualquer campo total(tipo_desconto, desconto, frete, etc.)
        $(document).on('change keyup paste', 'input[id$=-subtotal],#id_tipo_desconto,#id_desconto,#id_frete,#id_despesas,#id_seguro', function(){
            _this.setTotalFields();
        });

        //Atualiza o desconto total e o valor total da venda ao deletar formsets.
        $('.formset').on('change', function(){
            _this.setAdicionaisTotal();
            _this.setTotalFields();
        });

        //Preencher data inicial dos forms criados (para ItensVenda)
        $('.formset').on('formCreated', function(){
            $.Admin.vendaForm.setInitialItensData($(this));
        });

        //Mostrar modal do imposto ao clicar no icone
        $('.imposto-icon').on('click', function(){
            _this.mostrarModalImposto($(this).parents('.formset'));
        });

        //Alterar campos imposto, dependendo da opcao de calculo automatico
        $('#id_auto_calcular_modal').on('change', function(){
            $.Admin.vendaForm.alterarFieldsModal($(this).is(':checked'));
        });

        $('#calcular-parcelas').on('click', function(){
            $.Admin.vendaForm.setTotalParcelasFields();
        });

        $('#salvar_impostos_modal').on('click', function(){
            _this.salvarInfoImpostoModal($(this).parents('.imposto_modal'));
        });

        $('#compra_form_edit, #compra_form_add').on('submit', function(){
            return $.Admin.vendaForm.verificarParcelas();
        });

        //Abrir pdf em nova tab
        $('#gerar_pdf_compra').on('click', function(event){
            event.preventDefault();
            window.open($(this).prop('href'), $(this).prop('title'));
            return false;
        });
    },

    mostrarModalImposto: function(prod_formset){
        var form_numb = prod_formset.prop('id').match(/\d+/);
        var subtotal = prod_formset.find('input[id$=-subtotal]');
        var subtotal_s = prod_formset.find('input[id$=-total_sem_desconto]');

        $(".imposto_modal").modal('show').prop('id', form_numb);

        //Auto calcular impostos?
        $('#id_auto_calcular_modal').prop('checked', prod_formset.find('input[id$=-auto_calcular_impostos]').is(":checked")).change();

        //Rateio
        $('#id_rateio_desconto_modal').val(parseFloat(parseFloat(subtotal_s.val().replace(/\./g,'').replace(',','.')) - parseFloat(subtotal.val().replace(/\./g,'').replace(',','.'))).toFixed(2).replace(/\./g,','));

        //Cálculo
        $('#id_ipi_incluso_modal').prop('checked', prod_formset.find('input[id$=-ipi_incluido_preco]').is(":checked"));
        $('#id_icms_incluso_modal').prop('checked', prod_formset.find('input[id$=-icms_incluido_preco]').is(":checked"));
        $('#id_ipi_bc_icms_modal').prop('checked', prod_formset.find('input[id$=-incluir_bc_icms]').is(":checked"));

        //Impostos
        $('#id_pipi_modal').val(prod_formset.find('input[id$=-p_ipi]').val().replace(/\./g,','));
        $('#id_vipi_modal').val(prod_formset.find('input[id$=-vipi]').val().replace(/\./g,','));

        $('#id_p_red_bc').val(prod_formset.find('input[id$=-p_red_bc]').val().replace(/\./g,','));
        $('#id_picms_modal').val(prod_formset.find('input[id$=-p_icms]').val().replace(/\./g,','));
        $('#id_vicms_modal').val(prod_formset.find('input[id$=-vicms]').val().replace(/\./g,','));

        //Totais
        $('#id_total_impostos_modal').val(prod_formset.find('input[id$=-total_impostos]').val().replace(/\./g,','));
        $('#id_subtotal_modal').val(subtotal.val().replace(/\./g,','));
        $('#id_total_modal').val(prod_formset.find('input[id$=-total_com_impostos]').val().replace(/\./g,','));
    },

    salvarInfoImpostoModal: function(modal){
        var form_atual = $('#produtos_form-' + modal.prop('id'));

        form_atual.find('input[id$=-auto_calcular_impostos]').prop('checked', modal.find('#id_auto_calcular_modal').is(':checked'));

        //Rateio
        form_atual.find('input[id$=-desconto]').val(modal.find('#id_rateio_desconto_modal').val());

        //Opcoes
        form_atual.find('input[id$=-ipi_incluido_preco]').prop('checked', modal.find('#id_ipi_incluso_modal').is(':checked'));
        form_atual.find('input[id$=-icms_incluido_preco]').prop('checked', modal.find('#id_icms_incluso_modal').is(':checked'));
        form_atual.find('input[id$=-incluir_bc_icms]').prop('checked', modal.find('#id_ipi_bc_icms_modal').is(':checked'));

        //IPI
        form_atual.find('input[id$=-p_ipi]').val(modal.find('#id_pipi_modal').val());
        form_atual.find('input[id$=-vipi]').val(modal.find('#id_vipi_modal').val());

        //ICMS
        form_atual.find('input[id$=-p_icms]').val(modal.find('#id_picms_modal').val());
        form_atual.find('input[id$=-vicms]').val(modal.find('#id_vicms_modal').val());

        form_atual.find('select[id$=-tipo_desconto]').val('0').trigger('change');
    },

    setItensFields: function(form_number){
        var form_atual = $('div[id=produtos_form-' + form_number + ']');
        var val_unit = form_atual.find('input[id$=-valor_unit]');
        var qtd = form_atual.find('input[id$=-quantidade]');
        var tipo_desconto = form_atual.find('select[id$=-tipo_desconto]');
        var desconto = form_atual.find('input[id$=-desconto]');
        var subtotal = form_atual.find('input[id$=-subtotal]');
        var total_sem_desconto = form_atual.find('input[id$=-total_sem_desconto]');
        var total = form_atual.find('input[id$=-total_com_impostos]');
        var total_impostos = form_atual.find('input[id$=-total_impostos]');
        var vprod = parseFloat(parseFloat(qtd.val().replace(/\./g,'').replace(',','.'))*parseFloat(val_unit.val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        var vtotal = vprod;
        var vtotal_impostos = 0;
        var vsubtotal_sem_desconto = 0;
        var vtotal_sem_impostos = 0;

        var vdesconto = parseFloat($(desconto).val().replace(/\./g,'').replace(',','.'));

        if(tipo_desconto.val() == '0' && !isNaN(vdesconto)){
            vtotal = parseFloat(parseFloat(vtotal) - parseFloat(vdesconto)).toFixed(2);
        }else if(tipo_desconto.val() == '1' && !isNaN(vdesconto)){
            vdesconto = parseFloat((parseFloat(vdesconto)/100)*parseFloat(vtotal).toFixed(2)).toFixed(2);
            vtotal = parseFloat(parseFloat(vtotal) - parseFloat(vdesconto)).toFixed(2);
        }

        if(!isNaN(vtotal)){
            vsubtotal_sem_desconto = parseFloat(vtotal) + parseFloat(vdesconto);
            vtotal_sem_impostos = parseFloat(vtotal);
        }

        /*   Impostos   */
        if(form_atual.find('select[id$=-produto]').val() && form_atual.find('input[id$=-auto_calcular_impostos]').is(':checked')){
            var pipi = form_atual.find('input[id$=-p_ipi]').val();
            var picms = form_atual.find('input[id$=-p_icms]').val();
            var vipi = 0;
            var vicms = 0;
            var red_bc_icms = parseFloat(parseFloat(form_atual.find('input[id$=-p_red_bc]').val())/100);
            var ipi_bc_icms = form_atual.find('input[id$=-incluir_bc_icms]').is(':checked');
            var tipo_ipi = form_atual.find('select[id$=-tipo_ipi]').val();

            //Calculo IPI
            if(tipo_ipi == '0'){
                form_atual.find('input[id$=-vipi]').val('0.00');
            }else if(tipo_ipi == '1'){
                vfixo_ipi = form_atual.find('input[id$=-vfixo_ipi]').val().replace(',','.');
                vipi = parseFloat(parseFloat(vfixo_ipi)*parseFloat(qtd.val().replace(/\./g,'').replace(',','.')));
                form_atual.find('input[id$=-vipi]').val(parseFloat(vipi).toFixed(2));
                if(form_atual.find('input[id$=-ipi_incluido_preco]').is(':checked')){
                    vtotal_sem_impostos = parseFloat(vtotal_sem_impostos) - parseFloat(vipi);
                }
            }else if(tipo_ipi == '2'){
                if(form_atual.find('input[id$=-ipi_incluido_preco]').is(':checked')){
                    vipi = parseFloat(parseFloat(vprod)*parseFloat(pipi)/(100+parseFloat(pipi))).toFixed(2);
                    form_atual.find('input[id$=-vipi]').val(parseFloat(vipi).toFixed(2));
                    vtotal_sem_impostos = parseFloat(vtotal_sem_impostos) - parseFloat(vipi);
                }else{
                    vipi = parseFloat(parseFloat(vsubtotal_sem_desconto)*parseFloat(pipi)/100).toFixed(2);
                    form_atual.find('input[id$=-vipi]').val(parseFloat(vipi).toFixed(2));
                }
            }
            vtotal_impostos = parseFloat(vtotal_impostos) + parseFloat(vipi);

            //Calculo ICMS
            if(parseFloat(picms) > 0){
                if(form_atual.find('input[id$=-icms_incluido_preco]').is(':checked')){
                    vicms = parseFloat(parseFloat(vprod)*parseFloat(picms)/(100+parseFloat(picms))).toFixed(2);
                    form_atual.find('input[id$=-vicms]').val(parseFloat(vicms).toFixed(2));
                    vtotal_sem_impostos = parseFloat(vtotal_sem_impostos) - parseFloat(vicms);
                }else if(ipi_bc_icms){
                    var vbc_icms = parseFloat(vtotal) + parseFloat(vipi);
                    vbc_icms = parseFloat(vbc_icms) - parseFloat(vbc_icms)*parseFloat(red_bc_icms);
                    vicms = parseFloat(parseFloat(vbc_icms)*parseFloat(picms)/100).toFixed(2);
                    form_atual.find('input[id$=-vicms]').val(parseFloat(vicms).toFixed(2));
                }else{
                    var vbc_icms = parseFloat(vtotal);
                    vbc_icms = parseFloat(vbc_icms) - parseFloat(vbc_icms)*parseFloat(red_bc_icms);
                    vicms = parseFloat(parseFloat(vbc_icms)*parseFloat(picms)/100).toFixed(2);
                    form_atual.find('input[id$=-vicms]').val(parseFloat(vicms).toFixed(2));
                }
            }
            vtotal_impostos = parseFloat(vtotal_impostos) + parseFloat(vicms);

            vsubtotal_sem_desconto = parseFloat(vtotal_sem_impostos) + parseFloat(vdesconto);
            vtotal = parseFloat(vtotal_sem_impostos) + parseFloat(vtotal_impostos);

        }else{
            //Caso totais ja foram preenchidos pelo usuario
            var vipi = form_atual.find('input[id$=-vipi]').val().replace(/\./g,'').replace(',','.');
            var vicms = form_atual.find('input[id$=-vicms]').val().replace(/\./g,'').replace(',','.');
            vtotal_impostos = parseFloat(vipi) + parseFloat(vicms);

            if(form_atual.find('input[id$=-ipi_incluido_preco]').is(':checked')){
                vtotal_sem_impostos = parseFloat(vtotal_sem_impostos) - parseFloat(vipi);
            }
            if(form_atual.find('input[id$=-icms_incluido_preco]').is(':checked')){
                vtotal_sem_impostos = parseFloat(vtotal_sem_impostos) - parseFloat(vicms);
            }

            vsubtotal_sem_desconto = parseFloat(vtotal_sem_impostos) + parseFloat(vdesconto);
            vtotal = parseFloat(vtotal_sem_impostos) + parseFloat(vtotal_impostos);

        }

        //Totais
        total_impostos.val(parseFloat(vtotal_impostos).toFixed(2).replace('.',','));
        total_sem_desconto.val(parseFloat(vsubtotal_sem_desconto).toFixed(2).replace('.',','))
        subtotal.val(parseFloat(vtotal_sem_impostos).toFixed(2).replace('.',','));
        total.val(parseFloat(vtotal).toFixed(2).replace('.',','));

        subtotal.change();
    },

    setTotalFields: function(){
        var tipo_desconto = $('#id_tipo_desconto');
        var desconto = $('#id_desconto');
        var vtotal = 0;

        $('input[id$=-total_sem_desconto]:visible').each(function(){
            var vtotal_sem_desconto = parseFloat($(this).val().replace(/\./g,'').replace(',','.')).toFixed(2);
            if(!isNaN(vtotal_sem_desconto)){
                vtotal = parseFloat(parseFloat(vtotal) + parseFloat(vtotal_sem_desconto)).toFixed(2);
            }
        });

        if(tipo_desconto.val() == '0'){
            vtotal = parseFloat(parseFloat(vtotal) - parseFloat($(desconto).val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        }else if(tipo_desconto.val() == '1'){
            vtotal = parseFloat(parseFloat(vtotal) - (parseFloat($(desconto).val().replace(/\./g,'').replace(',','.'))/100)*parseFloat(vtotal)).toFixed(2);
        }

        vtotal = parseFloat(parseFloat(vtotal) + parseFloat($('#id_frete').val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        vtotal = parseFloat(parseFloat(vtotal) + parseFloat($('#id_despesas').val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        vtotal = parseFloat(parseFloat(vtotal) + parseFloat($('#id_seguro').val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        vtotal = parseFloat(parseFloat(vtotal) + parseFloat($('#id_total_icms').val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        vtotal = parseFloat(parseFloat(vtotal) + parseFloat($('#id_total_ipi').val().replace(/\./g,'').replace(',','.'))).toFixed(2);

        if(!isNaN(vtotal)){
            $('#id_valor_total').val(vtotal.replace(/\./g,','));
            $('#id_valor_total_display').text(vtotal.replace(/\./g,','));
        }
    },

    setAdicionaisTotal: function(){
        var tipo_desconto_tot = $('#id_tipo_desconto').val();
        var desconto_total = $('#id_desconto');
        var vdesconto_total = 0;
        var ipi_total = $('#id_total_ipi');
        var vipi_total = 0;
        var icms_total = $('#id_total_icms');
        var vicms_total = 0;
        var vtotal_sem_desconto = 0;

        $('.formset[id^=produtos_form-]:visible').each(function(){
            var tipo_desconto = $(this).find('select[id$=-tipo_desconto]').eq(0).val()
            var desconto = $(this).find('input[id$=-desconto]').eq(0);
            var vdesconto = 0;
            var vipi_item = $(this).find('input[id$=-vipi]').eq(0).val();
            var vicms_item = $(this).find('input[id$=-vicms]').eq(0).val();
            var vsubtotal_sem_desconto = $(this).find('input[id$=-total_sem_desconto]').eq(0).val().replace(/\./g,'').replace(',','.');

            if(!isNaN(parseFloat(vicms_item))){
                vicms_total = parseFloat(vicms_total) + parseFloat(vicms_item.replace(',','.'));
            }

            if(!isNaN(parseFloat(vipi_item))){
                vipi_total = parseFloat(vipi_total) + parseFloat(vipi_item.replace(',','.'));
            }

            if(tipo_desconto == '0'){
                vdesconto = parseFloat(parseFloat($(desconto).val().replace(/\./g,'').replace(',','.'))).toFixed(2);
            }else if(tipo_desconto == '1'){
                vdesconto = (parseFloat($(desconto).val().replace(/\./g,'').replace(',','.'))/100)*parseFloat(vsubtotal_sem_desconto);
            }

            if(!isNaN(vdesconto)){
                vdesconto_total = parseFloat(vdesconto_total) + parseFloat(vdesconto);
            }

            vtotal_sem_desconto = parseFloat(vtotal_sem_desconto) + parseFloat(vsubtotal_sem_desconto);

        });

        vdesconto_total = parseFloat(vdesconto_total);

        if(tipo_desconto_tot == '0' && !isNaN(vdesconto_total)){
            desconto_total.val(parseFloat(vdesconto_total).toFixed(2).replace(/\./g,','));
        }else if(tipo_desconto_tot == '1' && !isNaN(vdesconto_total)){
            var pdesconto_total = parseFloat((parseFloat(vdesconto_total)*100)/parseFloat(vtotal_sem_desconto)).toFixed(4);

            if(!isNaN(pdesconto_total)){
                desconto_total.val(pdesconto_total.replace('.',','));
            }
        }

        if(!isNaN(vicms_total)){
            icms_total.val(parseFloat(vicms_total).toFixed(2).replace(/\./g,','));
        }
        if(!isNaN(vipi_total)){
            ipi_total.val(parseFloat(vipi_total).toFixed(2).replace(/\./g,','));
        }
    },

    handleProdutoInfo: function(data, form_number, initial){
        var val_unit = $('#id_produtos_form-'+ form_number + '-valor_unit');
        var form_atual = $('div[id=produtos_form-' +form_number+ ']');

        if(!initial){
            form_atual.find('input[type=text]').val('0');
            form_atual.find('input[id$=-quantidade]').val(1);
            form_atual.find('input[type=checkbox]').not('input[id$=-auto_calcular_impostos]').prop('checked',false);
        }

        if(typeof data === 'undefined' || !data){
            return;
        }else{
            if(data[0].fields.venda && !initial) val_unit.val(data[0].fields.venda.replace(/\./g,','));
            for(var i = 0; i < data.length; i++) {
                if(data[i].model == 'fiscal.icms' || data[i].model == 'fiscal.icmssn'){
                    if(data[i].fields.p_icms && !initial) form_atual.find('input[id$=-p_icms]').val(data[i].fields.p_icms);
                    if(data[i].fields.p_red_bc) form_atual.find('input[id$=-p_red_bc]').val(data[i].fields.p_red_bc);
                    if(data[i].fields.p_icmsst && !initial) form_atual.find('input[id$=-p_icmsst]').val(data[i].fields.p_icmsst);
                    if(data[i].fields.p_red_bcst) form_atual.find('input[id$=-p_red_bcst]').val(data[i].fields.p_red_bcst);
                    if(data[i].fields.p_mvast) form_atual.find('input[id$=-p_mvast]').val(data[i].fields.p_mvast);
                }

                if(data[i].model == 'fiscal.icms' && !initial){
                    form_atual.find('input[id$=-icms_incluido_preco]').prop('checked', data[i].fields.icms_incluido_preco);
                    form_atual.find('input[id$=-icmsst_incluido_preco]').prop('checked', data[i].fields.icmsst_incluido_preco);

                }else if(data[i].model == 'fiscal.icmssn' && !initial){
                    form_atual.find('input[id$=-icms_incluido_preco]').prop('checked', data[i].fields.icmssn_incluido_preco);
                    form_atual.find('input[id$=-icmsst_incluido_preco]').prop('checked', data[i].fields.icmssnst_incluido_preco);

                }else if(data[i].model == 'fiscal.ipi'){
                    if(!initial) form_atual.find('input[id$=-ipi_incluido_preco]').prop('checked', data[i].fields.ipi_incluido_preco);
                    if(!initial) form_atual.find('input[id$=-incluir_bc_icms]').prop('checked', data[i].fields.incluir_bc_icms);
                    if(!initial) form_atual.find('input[id$=-incluir_bc_icmsst]').prop('checked', data[i].fields.incluir_bc_icmsst);

                    form_atual.find('select[id$=-tipo_ipi]').val(data[i].fields.tipo_ipi);

                    if(data[i].fields.tipo_ipi == '0'  && !initial){
                        form_atual.find('input[id$=-p_ipi]').val('0.00');
                    }else if(data[i].fields.tipo_ipi == '1'  && !initial){
                        if(data[i].fields.valor_fixo) form_atual.find('input[id$=-vfixo_ipi]').val(data[i].fields.valor_fixo);
                    }else if(data[i].fields.tipo_ipi == '2'  && !initial){
                        if(data[i].fields.p_ipi) form_atual.find('input[id$=-p_ipi]').val(data[i].fields.p_ipi);
                    }
                }else if(data[i].model == 'fiscal.icmsufdest'){
                    if(data[i].fields.p_fcp_dest) form_atual.find('input[id$=-pfcp]').val(data[i].fields.p_fcp_dest);
                    if(data[i].fields.p_icms_dest) form_atual.find('input[id$=-p_icms_dest]').val(data[i].fields.p_icms_dest);
                    if(data[i].fields.p_icms_inter) form_atual.find('input[id$=-p_icms_inter]').val(data[i].fields.p_icms_inter);
                    if(data[i].fields.p_icms_inter_part) form_atual.find('input[id$=-p_icms_part]').val(data[i].fields.p_icms_inter_part);
                }

            }
            //Para trigger o metodo setItensFields
            if(!initial) form_atual.find('input[id$=-quantidade]').change();
        }

    },

    handleFornecedorInfo: function(data){
        if(typeof data === 'undefined' || !data){
            $('.display-fornecedor-field').text('');
        }else{
            $('.display-fornecedor-field').text('');
            for(var i = 0; i < data.length; i++) {
                if(data[i].model == 'cadastro.pessoajuridica'){
                    $('#cpf_cnpj_fornecedor').text(data[i].fields.cnpj);
                    $('#ie_rg_fornecedor').text(data[i].fields.inscricao_estadual);
                    $('#representante_fornecedor').text(data[i].fields.responsavel)
                }else if(data[i].model == 'cadastro.pessoafisica'){
                    $('#cpf_cnpj_fornecedor').text(data[i].fields.cpf);
                    $('#ie_rg_fornecedor').text(data[i].fields.rg);
                }

                if(data[i].model == 'cadastro.endereco'){
                    $('#endereco_fornecedor').text(data[i].fields.logradouro + ' ' + data[i].fields.numero);
                    $('#bairro_fornecedor').text(data[i].fields.bairro);
                    $('#municipio_fornecedor').text(data[i].fields.municipio);
                    $('#uf_fornecedor').text(data[i].fields.uf);
                    $('#cep_fornecedor').text(data[i].fields.cep);
                }

                if(data[i].model == 'cadastro.email'){
                    $('#email_fornecedor').text(data[i].fields.email);
                }

                if(data[i].model == 'cadastro.telefone'){
                    $('#telefone_fornecedor').text(data[i].fields.telefone);
                }
            }
        }
    },
}


$.Admin.movimentoEstoqueForm = {
    init: function(req_urls){
        var _this = this;
        var produtos_input = $('select.select-produto');
        var transacao_input = $('select[id^=id_pedido_]');

        //Preencher campos iniciais dos itens com 0,00
        $('.formset[id^=itens_form-]').each(function(){
            var form_number = $(this).prop('id').match(/\d/)[0];
            if($(this).find('select[id$=-produto]').val().length === 0){
                _this.setInitialItensData($(this));
            }
        });

        produtos_input.on('change', function(event, initial){
            var form_number = $(this).prop('id').match(/\d/)[0];
            if($(this).val()){
                var postData = {
                    'produtoId': $(this).val(),
                }
                $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_produto_url'], postData, _this.handleProdutoInfo, form_number, initial);
            }else{
                _this.handleProdutoInfo(null, form_number, initial);
            }
        });

        produtos_input.trigger('change', [true]);

        //Ajax request Pedido: venda ou compra
        transacao_input.on('change', function(event){
            if($(this).prop('id').match('venda')){
                if($(this).val()){
                    var postData = {
                        'vendaId': $(this).val(),
                    }
                    $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_venda_url'], postData, _this.handlePedidoInfo);
                }else{
                    _this.handlePedidoInfo(null);
                }
            }else if($(this).prop('id').match('compra')){
                if($(this).val()){
                    var postData = {
                        'compraId': $(this).val(),
                    }
                    $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_compra_url'], postData, _this.handlePedidoInfo);
                }else{
                    _this.handlePedidoInfo(null);
                }
            }
        });

        /*  Eventos  */

        //Caso campo esteja vazio manter 0
        $(document).on('change keyup', 'input[id$=-quantidade],input[id$=-valor_unit]', function(){
            if(!$(this).val()) $(this).val('0');
        });

        //Atualiza valor total por item e adicionais totais
        $(document).on('load change keyup paste', 'input[id$=-quantidade],input[id$=-valor_unit]', function(){
            var form_number = $(this).prop('id').match(/\d/)[0];
            _this.setItensFields(form_number);
        });

        //Atualiza o valor total da venda ao modificar o total dos itens, ou qualquer campo total(tipo_desconto, desconto, frete, etc.)
        $(document).on('change keyup paste', 'input[id$=-subtotal]', function(){
            _this.setTotalFields();
        });

        //Preencher data inicial dos forms criados (para ItensMovimento) e atualizar valores totais
        $('.formset').on('formCreated', function(){
            _this.setInitialItensData($(this));
            _this.setTotalFields();
        });

        $('.formset').on('formRemoved', function(){
            _this.setTotalFields();
        });

    },

    setInitialItensData: function(prod_formset){
        prod_formset.find('input[id$=-quantidade]').val(1);
        prod_formset.find('input[id$=-valor_unit]').val('0,00');
        prod_formset.find('input[id$=-subtotal]').val('0,00');
    },

    setItensFields: function(form_number){
        var form_atual = $('div[id=itens_form-' + form_number + ']');
        var qtd = form_atual.find('input[id$=-quantidade]');
        var val_unit = form_atual.find('input[id$=-valor_unit]');
        var subtotal = form_atual.find('input[id$=-subtotal]');
        var vsubtotal = parseFloat(parseFloat(qtd.val().replace(/\./g,'').replace(',','.'))*parseFloat(val_unit.val().replace(/\./g,'').replace(',','.'))).toFixed(2);
        subtotal.val(parseFloat(vsubtotal).toFixed(2).replace('.',','));
        subtotal.change();
    },

    setTotalFields: function(){
        var v_itens = 0;
        var v_total = 0;
        $('input[id$=-subtotal]:visible').each(function(){
            var v_subtotal = parseFloat($(this).val().replace(/\./g,'').replace(',','.')).toFixed(2);
            if(!isNaN(v_subtotal)){
                v_total = parseFloat(parseFloat(v_total) + parseFloat(v_subtotal)).toFixed(2);
            }
            v_itens++;
        });
        $('#id_quantidade_itens').val(parseInt(v_itens));
        $('#id_valor_total').val(v_total.replace(/\./g,','));
    },

    handlePedidoInfo: function(data){
        $('.formset').each(function(){
            if($(this).prop('id') === 'itens_form-0'){
                $(this).find(':input:not([type=hidden])').each(function(){
                    $(this).prop({'value': '0'}).val('0').prop('checked',false);
                });

                $(this).find('.formset:last .add-formset').show();
            }else{
                var entryId = $(this).find('input:hidden[id $="-id"]');

                if(entryId.length){
                    $(this).find('input:checkbox[id $="-DELETE"]').prop('checked', true);
                }else{
                    $(this).find(':input').each(function(){
                        $(this).prop({'value': ''}).val('').prop('checked',false);
                    });
                    $(this).find('input:checkbox[id $="-DELETE"]').prop('checked', true);
                    $(this).trigger('newFormRemoved');
                }
                $(this).hide().change();
            }
        });

        if(data){
            var formsetBox = $('.formset-box');
            var formsetPrefix = formsetBox.find('.formset:last').prop('id');
            var nFormsets = (parseInt(formsetPrefix.substring(formsetPrefix.indexOf('-') + 1), 10) + 1).toString();
            var vitens = 0;
            var vitens_controlados = 0;
            var valor_total_itens = 0;
            formsetPrefix = formsetPrefix.substring(0, formsetPrefix.indexOf('-'));

            for(var i = 0; i < data.length; i++) {
                if(data[i].model == 'vendas.itensvenda' || data[i].model == 'compras.itenscompra'){
                    if(data[i].fields['controlar_estoque']){
                        vitens_controlados++;
                        valor_total_itens += parseFloat(data[i].fields['vprod'].replace(/\./g,'').replace(',','.'));

                        if(vitens_controlados === 1){
                            var newForm = formsetBox.find('.formset#itens_form-0');
                            if(parseInt(vitens) <= parseInt(vitens_controlados)){
                                newForm.find('.add-formset').show();
                            }else{
                                newForm.find('.add-formset').hide();
                            }
                        }else{
                            var parentFormset = formsetBox.find('.formset:last');

                            $.Admin.formset.createNewForm(parentFormset, nFormsets);

                            var newForm = parentFormset.next();
                            newForm.find('.add-formset').show();

                            //Adicionar form ao manager
                            nFormsets++;
                            $('#id_' + formsetPrefix + '-TOTAL_FORMS').val(nFormsets);

                            //Esconder add e remove do penultimo form
                            parentFormset.find('.add-formset').hide();
                        }

                        newForm.find('select[id$=-produto]').val(data[i].fields['produto_id']);
                        newForm.find('input[id$=-quantidade]').val(data[i].fields['quantidade']);
                        newForm.find('input[id$=-valor_unit]').val(data[i].fields['valor_unit']);
                        newForm.find('input[id$=-subtotal]').val(data[i].fields['vprod']);
                    }

                }
                else if(data[i].model == 'vendas.pedidovenda' || data[i].model == 'compras.pedidocompra'){
                    vitens = data[i].fields.n_itens;
                    $('select[id^=id_local_]').val(data[i].fields.local)
                }
            }

            $('#id_quantidade_itens').val(vitens_controlados);
            $('#id_valor_total').val(parseFloat(valor_total_itens).toFixed(2).replace('.',','));
        }

    },

    handleProdutoInfo: function(data, form_number, initial){
        if(!initial){
            var form_atual = $('div[id=itens_form-' +form_number+ ']');
            var estoque_atual_input = $('#id_itens_form-'+ form_number + '-estoque_atual');

            form_atual.find('input[type=text]').val('0');
            form_atual.find('input[id$=-quantidade]').val(1);
            if(data){
                if(data[0].fields.venda) $('#id_itens_form-'+ form_number + '-valor_unit').val(data[0].fields.venda.replace(/\./g,','));

                if(data[0].fields.controlar_estoque && data[0].fields.estoque_atual){
                    estoque_atual_input.val(data[0].fields.estoque_atual.replace(/\./g,','));
                    estoque_atual_input.removeClass('input_no_edit');
                }else{
                    estoque_atual_input.val('Não controlado');
                    estoque_atual_input.addClass('input_no_edit');
                }
            }
            form_atual.find('input[id$=-quantidade]').change();
        }
    },
}


$.Admin.lancamentoForm = {
    init: function(req_urls) {
        var _this = this;
        _this.calcularTotalLiquido();

        $(document).on('change keyup paste', '#id_valor_total,#id_abatimento,#id_juros,#id_valor_liquido', function(){
            if(!$(this).val()){
                $(this).val('0,00');
            }
            _this.calcularTotalLiquido();
        });

        $('#pagar_conta,#receber_conta').on('click', function(){
            $('.modal_selecionar_data').modal('show');
            $('#id_data_pagamento').val($('#id_data_vencimento').val());
            if($(this).prop('id') == 'receber_conta'){
                //Receber conta
                $('#id_tipo_conta').val('0');
            }else if($(this).prop('id') == 'pagar_conta'){
                //Pagar conta
                $('#id_tipo_conta').val('1');
            }

        });

        $('#baixar_conta_confirma').on('click', function(){
            var data_input = $('#id_data_pagamento');
            if(!data_input.val() || !/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(data_input.val())){
                data_input.css('border-color','red');
            }else{
                var postData = {
                    'tipoConta': $('#id_tipo_conta').val(),
                    'contaId': $('#id_conta_id').val(),
                    'dataPagamento': $('#id_data_pagamento').val(),
                }
                $.Admin.ajaxRequest.ajaxPostRequest(req_urls['gerar_lancamento_url'], postData, _this.handleGerarLancamento);
            }
        });
    },

    calcularTotalLiquido: function(){
        var vabatimento = $('#id_abatimento').val().replace(/\./g,'').replace(',','.');
        var vjuros = $('#id_juros').val().replace(/\./g,'').replace(',','.');
        var vbruto = $('#id_valor_total').val().replace(/\./g,'').replace(',','.');
        var vl_input = $('#id_valor_liquido');
        var vliquido = 0;

        vliquido = parseFloat(vbruto) - parseFloat(vabatimento) + parseFloat(vjuros);
        vl_input.val(vliquido.toString().replace('.',','));
    },

    handleGerarLancamento: function(data){
        window.location.replace(data.url);
    },
}

$.Admin.lancamentoList = {
    init: function(req_urls) {
        var _this = this;

        $('#pagar_conta,#receber_conta').on('click', function(){
            var parent_row = $(this).parents('tr');
            $('.modal_selecionar_data').modal('show');
            $('#id_conta_id').val(parent_row.find('td:eq(0)').text());
            $('#id_data_pagamento').val(parent_row.find('td:eq(2)').text());
            if($(this).prop('id') == 'receber_conta'){
                //Receber conta
                $('#id_tipo_conta').val('0');
            }else if($(this).prop('id') == 'pagar_conta'){
                //Pagar conta
                $('#id_tipo_conta').val('1');
            }
        });

        $('#baixar_conta_confirma').on('click', function(){
            var data_input = $('#id_data_pagamento');
            if(!data_input.val() || !/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(data_input.val())){
                data_input.css('border-color','red');
            }else{
                var postData = {
                    'tipoConta': $('#id_tipo_conta').val(),
                    'contaId': $('#id_conta_id').val(),
                    'dataPagamento': $('#id_data_pagamento').val(),
                }
                $.Admin.ajaxRequest.ajaxPostRequest(req_urls['gerar_lancamento_url'], postData, _this.handleGerarLancamento);
            }
        });
    },

    handleGerarLancamento: function(data){
        window.location.replace(data.url);
    },
}


$.Admin.notaFiscalForm = {
    init: function(req_urls, tipo_nf) {
        var _this = this;
        if(tipo_nf == 'saida'){
            var emit_input = $('#id_emit_saida');
            var dest_input = $('#id_dest_saida');
            var transacao_input = $('#id_venda');
        }else if(tipo_nf == 'entrada'){
            var emit_input = $('#id_emit_entrada');
            var dest_input = $('#id_dest_entrada');
            var transacao_input = $('#id_compra');
        }
        var fat_dup_chk = $('#id_grupo_cobr');

        //Ajax request emitente(empresa ou fornecedor)
        emit_input.on('change', function(){
            if($(this).val()){
                var postData = {
                    'pessoaId': $(this).val(),
                }
                $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_emit_url'], postData, _this.handleEmitInfo);
            }else{
                _this.handleEmitInfo();
            }
        });

        emit_input.change();

        fat_dup_chk.on('change', function(){
            var fat_chkd = $(this).is(':checked');
            $('div.fatura_input_div').find('input').each(function(){
                if(fat_chkd){
                    $(this).prop('readonly', false);
                    $(this).removeClass('input_no_edit');
                }else{
                    $(this).prop('readonly', true);
                    $(this).addClass('input_no_edit');
                }
            });
        });

        fat_dup_chk.change();

        //Ajax request destinatario(cliente ou empresa)
        dest_input.on('change', function(){
            if($(this).val()){
                var postData = {
                    'pessoaId': $(this).val(),
                }
                $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_dest_url'], postData, _this.handleDestInfo);
            }else{
                _this.handleEmitInfo();
            }
        });
        dest_input.change();

        //Ajax request Transacao: venda ou compra
        transacao_input.on('change', function(event, initial){
            if(tipo_nf == 'saida'){
                if($(this).val()){
                    var postData = {
                        'vendaId': $(this).val(),
                    }
                    $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_venda_url'], postData, _this.handleVendaInfo, initial);
                }else{
                    _this.handleVendaInfo(null, initial);
                }
            }else if(tipo_nf == 'entrada'){
                if($(this).val()){
                    var postData = {
                        'compraId': $(this).val(),
                    }
                    $.Admin.ajaxRequest.ajaxPostRequest(req_urls['info_compra_url'], postData, _this.handleCompraInfo, initial);
                }else{
                    _this.handleCompraInfo(null, initial);
                }
            }
        });
        transacao_input.trigger('change', [true]);

        $('table').on('click', '.detalhes-icon', function(){
            _this.mostrarModalDetalhes($(this).parents('.itens_row'));
        });

        $('#salvar_detalhes_modal').on('click', function(){
            _this.salvarModalDetalhes($(this).parents('.detalhes_modal'));
        });

        //Page loaders para cada servico
        $('form[id=emitir_nota_form]').on('submit', function(){
            $('.page-loader-wrapper').show();
            $('.loader .loader-message').text('Enviando nota fiscal, aguarde...');
        });

        $('form[id=cancelar_nota_form]').on('submit', function(){
            $('.page-loader-wrapper').show();
            $('.loader .loader-message').text('Cancelando nota fiscal, aguarde...');
        });

        $('form[id=consultar_cadastro_form]').on('submit', function(){
            $('.page-loader-wrapper').show();
            $('.loader .loader-message').text('Consultando cadastro, aguarde...');
        });

        $('form[id=inutilizar_notas_form]').on('submit', function(){
            $('.page-loader-wrapper').show();
            $('.loader .loader-message').text('Inutilizando numeração de notas, aguarde...');
        });

        $('form[id=consultar_nota_form]').on('submit', function(){
            $('.page-loader-wrapper').show();
            $('.loader .loader-message').text('Consultando nota, aguarde...');
        });

        $('form[id=baixar_nota_form]').on('submit', function(){
            $('.page-loader-wrapper').show();
            $('.loader .loader-message').text('Baixando nota, aguarde...');
        });

        $('form[id=manifestacao_destinatario_form]').on('submit', function(){
            $('.page-loader-wrapper').show();
            $('.loader .loader-message').text('Enviando manifestação do destinatário, aguarde...');
        });

    },

    handleEmitInfo: function(data){
        if(typeof data === 'undefined' || !data){
            $('.display-emit-field').text('');
        }else{
            $('.display-emit-field').text('');
            for(var i = 0; i < data.length; i++) {
                if(data[i].model == 'cadastro.pessoajuridica'){
                    $('#cpf_cnpj_emit').text(data[i].fields.cnpj);
                    $('#ie_rg_emit').text(data[i].fields.inscricao_estadual);
                }else if(data[i].model == 'cadastro.pessoafisica'){
                    $('#cpf_cnpj_emit').text(data[i].fields.cpf);
                    $('#ie_rg_emit').text(data[i].fields.rg);
                }

                if(data[i].model == 'cadastro.endereco'){
                    $('#endereco_emit').text(data[i].fields.logradouro);
                    $('#nro_emit').text(data[i].fields.numero);
                    $('#bairro_emit').text(data[i].fields.bairro);
                    $('#cidade_emit').text(data[i].fields.municipio);
                    $('#cmun_emit').text(data[i].fields.cmun);
                    $('#estado_emit').text(data[i].fields.uf);
                    $('#cpl_emit').text(data[i].fields.complemento);
                    $('#pais_emit').text(data[i].fields.pais);
                    $('#cep_emit').text(data[i].fields.cep);
                }

                if(data[i].model == 'cadastro.email'){
                    $('#email_emit').text(data[i].fields.email);
                }

                if(data[i].model == 'cadastro.telefone'){
                    $('#tel_emit').text(data[i].fields.telefone);
                }
            }
        }
    },

    handleDestInfo: function(data){
        if(typeof data === 'undefined' || !data){
            $('.display-dest-field').text('');
            $('#cpf_cnpj_id_dest').text('');
        }else{
            $('.display-dest-field').text('');
            for(var i = 0; i < data.length; i++) {
                if(data[i].model == 'cadastro.pessoajuridica'){
                    $('#cpf_cnpj_id_dest').text(data[i].fields.cnpj);
                    $('#ie_rg_dest').text(data[i].fields.inscricao_estadual);
                }else if(data[i].model == 'cadastro.pessoafisica'){
                    $('#cpf_cnpj_id_dest').text(data[i].fields.cpf);
                    $('#ie_rg_dest').text(data[i].fields.rg);
                }

                if(data[i].model == 'cadastro.cliente'){
                    var ind_ie = data[i].fields.indicador_ie;
                    if(ind_ie == '1'){
                        $('#ind_ie_dest').text('Contribuinte ICMS');
                    }else if(ind_ie == '2'){
                        $('#ind_ie_dest').text('Contribuinte isento de Inscrição');
                    }else if(ind_ie == '9'){
                        $('#ind_ie_dest').text('Não Contribuinte');
                    }
                    if(data[i].fields.id_estrangeiro){
                        $('#cpf_cnpj_id_dest').text(data[i].fields.id_estrangeiro);
                    }
                }

                if(data[i].model == 'cadastro.endereco'){
                    $('#endereco_dest').text(data[i].fields.logradouro);
                    $('#nro_dest').text(data[i].fields.numero);
                    $('#bairro_dest').text(data[i].fields.bairro);
                    $('#cidade_dest').text(data[i].fields.municipio);
                    $('#cmun_dest').text(data[i].fields.cmun);
                    $('#estado_dest').text(data[i].fields.uf);
                    $('#cpl_dest').text(data[i].fields.complemento);
                    $('#pais_dest').text(data[i].fields.pais);
                    $('#cep_dest').text(data[i].fields.cep);
                }

                if(data[i].model == 'cadastro.email'){
                    $('#email_dest').text(data[i].fields.email);
                }

                if(data[i].model == 'cadastro.telefone'){
                    $('#tel_dest').text(data[i].fields.telefone);
                }
            }
        }
    },

    handleVendaInfo: function(data, initial){
        if(typeof data === 'undefined' || !data){
            $('.display-venda-field').text('');
            $('#itens_table > tbody').empty();
            $('#pagamentos_tabela > tbody').empty();
        }else{
            $('.display-venda-field').text('');
            $('#itens_table > tbody').empty();
            $('#pagamentos_tabela > tbody').empty();
            for(var i = 0; i < data.length; i++) {
                if(data[i].model == 'vendas.itensvenda'){
                    var itens_venda_id = data[i].pk
                    var new_tr = "<tr class=\"itens_row\" id=\"" + itens_venda_id + "\">";

                    var ordered_fields = ['produto', 'quantidade', 'valor_unit', 'desconto', 'impostos', 'total']
                    for (var j = 0; j < ordered_fields.length; j++) {
                        if(data[i].fields[ordered_fields[j]]){
                            new_tr += "<td id="+ ordered_fields[j] +">" + data[i].fields[ordered_fields[j]] + "</td>";
                        }else{
                            new_tr += "<td id="+ ordered_fields[j] +"></td>";
                        }
                    }

                    new_tr += "<td><i class=\"material-icons detalhes-icon\">&#xE88E;</i></td>"

                    for(var hidden_field in data[i].hidden_fields){
                        if(data[i].hidden_fields[hidden_field]){
                            new_tr += "<td class=\"hidden\" id="+ hidden_field +">" + data[i].hidden_fields[hidden_field] + "</td>";
                        }else{
                            new_tr += "<td class=\"hidden\" id="+ hidden_field +"></td>";
                        }
                    }

                    for(var field in data[i].editable_fields){
                        if(data[i].editable_fields[field]){
                            new_tr += "<td class=\"hidden\" id="+ field +"><input type=\"text\" name="+ field +"_"+ itens_venda_id +" value=\"" + data[i].editable_fields[field].replace(/\./g,'') + "\"/></td>";
                        }else{
                            new_tr += "<td class=\"hidden\" id="+ field +"><input type=\"text\" name="+ field +"_"+ itens_venda_id +" value=\"\"/></td>";
                        }
                    }

                    new_tr += "<td class=\"hidden\" id=\"id_pk_item\"><input type=\"text\" name=\"pk_item\" value=\"" + itens_venda_id + "\"/></td>";

                    new_tr += "</tr>";
                    $('#itens_table > tbody').append(new_tr);
                }else if(data[i].model == 'vendas.pedidovenda'){
                    if(data[i].fields.dest && !initial) $('#id_dest').val(data[i].fields.dest).change();
                    $('#status_venda').text(data[i].fields.status);
                    $('#desconto_venda').text(data[i].fields.desconto);
                    $('#frete_venda').text(data[i].fields.frete);
                    $('#despesas_venda').text(data[i].fields.despesas);
                    $('#seguro_venda').text(data[i].fields.seguro);
                    $('#impostos_venda').text(data[i].fields.impostos);

                    $('#total_venda').text(data[i].fields.valor_total);
                    $('#id_valor_pag').text(data[i].fields.valor_total);
                    $('#id_forma_pag').text(data[i].fields.forma_pag);

                    if(!initial){
                        $('#id_n_fat').val(data[i].pk);
                        $('#id_v_orig').val(data[i].fields.total_sem_desconto);
                        $('#id_v_desc').val(data[i].fields.desconto);
                        $('#id_v_liq').val(data[i].fields.valor_total);
                        $('#id_dest_saida').val(data[i].fields.dest).change();

                        if(data[i].fields.n_parcelas <= 1){
                            $('select[id=id_indpag]').val("0");
                        }else{
                            $('select[id=id_indpag]').val("1");
                        }

                        if(data[i].fields.ind_final){
                            $('#id_ind_final').val('1');
                        }else{
                            $('#id_ind_final').val('0');
                        }
                    }

                }else if(data[i].model == 'vendas.pagamento'){
                    var new_tr = "<tr class=\"pagamento_row\">";
                    var ordered_fields = ['id', 'vencimento', 'valor_parcela']

                    for (var j = 0; j < ordered_fields.length; j++) {
                        if(data[i].fields[ordered_fields[j]]){
                            new_tr += "<td id="+ ordered_fields[j] +">" + data[i].fields[ordered_fields[j]] + "</td>";
                        }else{
                            new_tr += "<td id="+ ordered_fields[j] +"></td>";
                        }
                    }

                    new_tr += "</tr>";

                    $('#pagamentos_tabela > tbody').append(new_tr);
                }
            }
        }
    },

    handleCompraInfo: function(data, initial){
        if(typeof data === 'undefined' || !data){
            $('.display-compra-field').text('');
            $('#itens_table > tbody').empty();
        }else{
            $('.display-compra-field').text('');
            $('#itens_table > tbody').empty();
            for(var i = 0; i < data.length; i++) {
                if(data[i].model == 'compras.itenscompra'){
                    var itens_venda_id = data[i].pk
                    var new_tr = "<tr class=\"itens_row\" id=\"" + itens_venda_id + "\">";

                    var ordered_fields = ['produto', 'quantidade', 'valor_unit', 'desconto', 'impostos', 'total']
                    for (var j = 0; j < ordered_fields.length; j++) {
                        if(data[i].fields[ordered_fields[j]]){
                            new_tr += "<td id="+ ordered_fields[j] +">" + data[i].fields[ordered_fields[j]] + "</td>";
                        }else{
                            new_tr += "<td id="+ ordered_fields[j] +"></td>";
                        }
                    }

                    new_tr += "<td><i class=\"material-icons detalhes-icon\">&#xE88E;</i></td>"

                    for(var hidden_field in data[i].hidden_fields){
                        if(data[i].hidden_fields[hidden_field]){
                            new_tr += "<td class=\"hidden\" id="+ hidden_field +">" + data[i].hidden_fields[hidden_field] + "</td>";
                        }else{
                            new_tr += "<td class=\"hidden\" id="+ hidden_field +"></td>";
                        }
                    }

                    for(var field in data[i].editable_fields){
                        if(data[i].editable_fields[field]){
                            new_tr += "<td class=\"hidden\" id="+ field +"><input type=\"text\" name="+ field +"_"+ itens_venda_id +" value=\"" + data[i].editable_fields[field].replace(/\./g,'') + "\"/></td>";
                        }else{
                            new_tr += "<td class=\"hidden\" id="+ field +"><input type=\"text\" name="+ field +"_"+ itens_venda_id +" value=\"\"/></td>";
                        }
                    }

                    new_tr += "<td class=\"hidden\" id=\"id_pk_item\"><input type=\"text\" name=\"pk_item\" value=\"" + itens_venda_id + "\"/></td>";

                    new_tr += "</tr>";
                    $('#itens_table > tbody').append(new_tr);
                }else if(data[i].model == 'compras.pedidocompra'){
                    if(data[i].fields.dest && !initial) $('#id_dest').val(data[i].fields.dest).change();
                    $('#status_compra').text(data[i].fields.status);
                    $('#desconto_compra').text(data[i].fields.desconto);
                    $('#frete_compra').text(data[i].fields.frete);
                    $('#despesas_compra').text(data[i].fields.despesas);
                    $('#seguro_compra').text(data[i].fields.seguro);
                    $('#vicms_compra').text(data[i].fields.total_icms);
                    $('#vipi_compra').text(data[i].fields.total_ipi);

                    $('#total_compra').text(data[i].fields.valor_total);
                }
            }
        }
    },

    mostrarModalDetalhes: function(table_row){
        var detalhes_modal = $('.detalhes_modal');
        detalhes_modal.modal('show');
        detalhes_modal.prop('id', table_row.prop('id').match(/\d+/));

        $('#id_codigo_modal').text(table_row.find('td[id=codigo]').text());
        $('#id_unidade_modal').text(table_row.find('td[id=unidade]').text());
        $('#id_ncm_modal').text(table_row.find('td[id=ncm]').text());
        $('#id_cfop_modal').text(table_row.find('td[id=cfop]').text());

        $('#id_desconto_modal').text(table_row.find('td[id=desconto]').text());
        $('#id_quantidade_modal').text(table_row.find('td[id=quantidade]').text());
        $('#id_valor_unit_modal').text(table_row.find('td[id=valor_unit]').text());
        $('#id_frete_modal').text(table_row.find('td[id=frete]').text());
        $('#id_seguro_modal').text(table_row.find('td[id=seguro]').text());
        $('#id_outras_despesas_modal').text(table_row.find('td[id=despesas]').text());

        $('#id_vicms_modal').text(table_row.find('td[id=vicms]').text());
        $('#id_vipi_modal').text(table_row.find('td[id=vipi]').text());
        $('#id_vicms_st_modal').text(table_row.find('td[id=vicms_st]').text());
        $('#id_vfcp_modal').text(table_row.find('td[id=vfcp]').text());
        $('#id_vicmsufdest_modal').text(table_row.find('td[id=vicmsufdest]').text());
        $('#id_vicmsufremet_modal').text(table_row.find('td[id=vicmsufremet]').text());
        $('#id_mot_des_icms_modal').text(table_row.find('td[id=mot_des_icms]').text());
        $('#id_vicms_deson_modal').val(table_row.find('td[id=editable_field_vicms_deson] input').val());

        $('#id_subtotal_modal').text(table_row.find('td[id=subtotal]').text());
        $('#id_total_impostos_modal').text(table_row.find('td[id=impostos]').text());
        $('#id_total_modal').text(table_row.find('td[id=total]').text());

        $('#id_vq_bcpis_modal').val(table_row.find('td[id=editable_field_vq_bcpis] input').val());
        $('#id_aliq_pis_modal').text(table_row.find('td[id=aliq_pis]').text());
        $('#id_vpis_modal').val(table_row.find('td[id=editable_field_vpis] input').val());
        $('#id_vq_bccofins_modal').val(table_row.find('td[id=editable_field_vq_bccofins] input').val());
        $('#id_aliq_cofins_modal').text(table_row.find('td[id=aliq_cofins]').text());
        $('#id_vcofins_modal').val(table_row.find('td[id=editable_field_vcofins] input').val());
        $('#id_inf_ad_prod_modal').val(table_row.find('td[id=editable_field_inf_ad_prod] input').val());
    },

    salvarModalDetalhes: function(modal){
        var row_atual = $('#itens_table tbody tr.itens_row#' + modal.prop('id'));

        row_atual.find('input[name^=\"editable_field_vpis\"]').val(modal.find('#id_vpis_modal').val());
        row_atual.find('input[name^=\"editable_field_vq_bcpis\"]').val(modal.find('#id_vq_bcpis_modal').val());
        row_atual.find('input[name^=\"editable_field_vq_bccofins\"]').val(modal.find('#id_vq_bccofins_modal').val());
        row_atual.find('input[name^=\"editable_field_vcofins\"]').val(modal.find('#id_vcofins_modal').val());

        row_atual.find('input[name^=\"editable_field_vicms_deson\"]').val(modal.find('#id_vicms_deson_modal').val());
        row_atual.find('input[name^=\"editable_field_inf_ad_prod\"]').val(modal.find('#id_inf_ad_prod_modal').val());
    }
}

$.Admin.fluxoCaixa = {
    init: function() {
        var _this = this;
    },
}


$.Admin.ajaxRequest = {
    ajaxGetRequest: function (req_url, handler) {
        var handler_arg = arguments[2];
        $.ajax({
            url: req_url,
            type: "GET",
            dataType: "json",
            success: function(data) {
                handler(data, handler_arg);
            },
        });
    },

    ajaxPostRequest: function (req_url, postData, handler) {
        var handler_arg = arguments[3];
        var handler_arg2 = arguments[4];
        postData.csrfmiddlewaretoken = $.Admin.cookies.getCookie('csrftoken');
        $.ajax({
            url: req_url,
            type: "POST",
            data: postData,
            dataType: "json",
            success: function(data) {
                handler(data, handler_arg, handler_arg2);
            },
        });
    }
}


$.Admin.datetimepicker = {
    init: function(){
        $('.datetimepicker').datetimepicker({
            format: 'd/m/Y H:i',
        });

        $.datetimepicker.setLocale('pt-BR');
    },
}

$.Admin.datepicker = {
    init: function(cookieName){
        $( ".datepicker" ).datepicker({
            dateFormat: 'dd/mm/yy',
            dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
            dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
            dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
            monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
            monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
            nextText: 'Próximo',
            prevText: 'Anterior'
        });
    },

    addDaysToDate: function(days){
        var _this = this;
        var d = new Date();
        var next = new Date(d.getTime() +  (days * 24 * 60 * 60 * 1000));
        var month = next.getMonth() + 1;
        var day = next.getDate();
        var year = next.getFullYear();
        return _this.padZeroNumber(day,2) + '/' + _this.padZeroNumber(month,2) + '/' + year;
    },

    padZeroNumber: function(str, max){
        str = str.toString();
        var pad = '0'.repeat(max)
        return pad.substring(0, pad.length - str.length) + str
    },
}

$.Admin.cookies = {
    getCookie: function(cookieName){
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, cookieName.length + 1) === (cookieName + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(cookieName.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
}
/* DinamicMenu()
* dinamic activate menu
*/
$.Admin.dinamicMenu = {
    init: function() {
        var url = window.location;

        // for sidebar menu entirely but not cover treeview
        $('.menu .list a').filter(function () {
          return this.href == url;
        }).parent().addClass('active');


        // for treeview
        var element = $('.menu .list a').filter(function () {
            var aux = this.href.split('/').slice(0, this.href.length-2).join("/");
          return this.href == url || url.href.indexOf(aux) ==
            0;
        });

        if (1 in element){
            element = $(element[1]);
            if (element.has("i").length == 0) {
                element.addClass('toggled waves-effect waves-block');
                element.parents('li').addClass('active');
                element.parent().parents('ul').show().siblings('a').addClass('toggled waves-effect waves-block')
            }
        }
    }
};

$(function () {
    $.Admin.barraLateral.init();
    $.Admin.navbar.init();
    $.Admin.table.init();
    $.Admin.formset.init();
    $.Admin.validation.init();
    $.Admin.dinamicMenu.init();

    setTimeout(function () { $('.page-loader-wrapper').fadeOut(); }, 50);
});