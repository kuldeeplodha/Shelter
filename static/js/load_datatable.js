
var columns_defs;
var table = null;
var divider = 1000 * 60 * 60 * 24;
var window = 8 * 1000 * 60 * 60 * 24;

var today = Date.now();
var daily_reporting_columns = [];






$(document).ready(function() {

    $("#delete_selected").hide();

   console.log("loading table...");
    var csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    $.ajax({
            url:"/mastersheet/columns",
            type : "GET",
            dataType : "json",
            data : "",
            contentType : "application/json",
            success : function (data,type,row,meta) {
                            columns_defs = data;
                            var tmp_daily_reporting_columns = [];
                            var tmp_account = [];
                            $.ajax({
                                url: "/mastersheet/buttons",
                                type: "GET",
                                dataType : "json",
                                contentType : "application/json",
                                async:false,
                                success : function(data){
                                    var DR = [];
                                    for(i = 53; i < (53 + data['daily_reporting']); i ++){
                                        DR.push(i);
                                    }
                                    tmp_daily_reporting_columns = DR;
                                    var ACC = [];
                                    for ( i = (53 + data['daily_reporting']); i < (53 + data['daily_reporting'] + data['accounts']); i++)
                                    {
                                        ACC.push(i);
                                    }
                                    tmp_accounts = ACC;

                                }
                            });
                            // Adding hyperlinks to community mobilization data
                            for (i = 0 ; i < tmp_daily_reporting_columns.length ; i ++ ){
                                columns_defs['data'][tmp_daily_reporting_columns[i]]['render']= function ( data, type, row,meta ) {
                                    if(typeof data != 'undefined') {
                                        url_daily_reporting = url_SBM = String("/admin/master/mastersheet/communitymobilization/") + row[columns_defs['data'][meta.col]['title']+"_id"] + String("/");
                                        if(type === 'display'){
                                                    data = '<a href = "#" onclick="window.open(\''+url_daily_reporting+'\', \'_blank\', \'width=650,height=550\');">' + data + "</a>";
                                        }
                                        return data;
                                    }
                                }
                            }
                            // Adding hyperlinks to accounts data
                            for (i = 0 ; i < tmp_accounts.length ; i ++ ){
                                columns_defs['data'][tmp_accounts[i]]['render']= function ( data, type, row,meta ) {
                                    if(typeof data != 'undefined'){
                                        url_accounts = String("/admin/master/mastersheet/vendorhouseholdinvoicedetail/") + row[columns_defs['data'][meta.col]['title']+"_id"] + String("/");
                                        if(type === 'display'){
                                                    data = '<a href = "#" onclick="window.open(\''+url_accounts+'\', \'_blank\', \'width=650,height=550\');">' + data + "</a>";

                                        }
                                        return data;
                                    }
                                }
                            }





                      }
    });
    $("#buttons").on("click","button",function(){

        $(this).toggleClass("active");
        flag = false;
        if ($(this).hasClass("active"))
        {
            flag = true;
        }
        section = $(this).attr('value');
        col = columns_defs['buttons'][section];
        table.columns(col).visible( flag );
    });

    function load_data_datatable(){

        if (table != null){
        table.ajax.reload();
        //flag_dates();

        }
        else{
            $(".overlay").show();
            buttons = '<div class="btn-group">';
            $.each(columns_defs['buttons'],function(index, button){
                buttons += '<button type="button" class="active btn btn-default" value="'+index+'">'+index+'</button>';
            });
            buttons += '</div>';
            $("#buttons").append(buttons);
            table = $("#example").DataTable( {


            "dom":"Bfrtip",
            "ajax" :  {

                            url : "/mastersheet/list/show/",
                            dataSrc:"",
                            data:{'form':$("#slum_form").serialize() , 'csrfmiddlewaretoken':csrf_token},
                            contentType : "application/json",
                            complete: function(){
                                $(".overlay").hide();
                                if(table.page.info().recordsDisplay != 0){
                                    //flag_dates();
                                }
                            }

                      },
            "columnDefs": [
                            {   "defaultContent": "-",
                                "targets": "_all",

                            } ,
                            {
                                "targets": [42,43,44],
                                "render": function ( data, type, row, meta ) {
                                                url_SBM = String("/admin/master/mastersheet/sbmupload/") + row.id + String("/");
                                                if(typeof data != 'undefined'){
                                                    if(type === 'display'){
                                                        data = '<a href = "#" onclick="window.open(\''+url_SBM+'\', \'_blank\', \'width=650,height=550\');">' + data + "</a>";
                                                    }

                                                    return data;
                                                }
                                            }

                            },
                            {
                                "targets": [45,46,47,48,49,50,51,52],
                                "render": function ( data, type, row, meta ) {
                                                url_TC = String("/admin/master/mastersheet/toiletconstruction/") + row['tc_id_'+String(row.Household_number)] + String("/");
                                                if(typeof data != 'undefined'){
                                                    if(type === 'display'){
                                                        '<a href = "#" onclick="window.open(\''+url_TC+'\', \'_blank\', \'width=650,height=550\');">' + data + "</a>";
                                                    }

                                                    return data;
                                                }
                                            }

                            },
                            {"footer":true},

                          ],

            "buttons":['excel'],

            "columns": columns_defs['data'],
            });


            //flag_dates();
            //highlight_buttons();
            add_search_box();
            $( table.table().container() ).on( 'keyup', 'tfoot tr th input', function (index,element) {

            table.column($(this).parent().index()).search( this.value ).draw();

            } );
            table.draw();
            $('#example').on("draw.dt", function(){
                for(i=0; i<10; i++)
                {
                    $('tr:eq('+i+')').css('background-color', '#ffffff');
                }
                flag_dates();
            });
            $('#example').on("draw.dt",function(){
                $('[data-toggle="popover"]').popover();// script for popover
            });

            $('#example').on( 'click', 'tbody td', function () {
                var data = table.cell( this ).render( 'sort' );
            } );


            $('#example tbody').on( 'click', 'tr', function () {
                $(this).toggleClass('selected');
            });
            $('#delete_selected').click( function () {


                var count = table.rows('.selected').data().length;
                if (count == 0){
                    alert("You have not selected any record. Please select a record to delete.");
                }
                else{
                    var records = [];
                    for( i = 0; i < count; i++){
                        records[i] = (table.rows('.selected').data()[i]['_id']);
                    }

                   //console.log(records.length);
                    if(records.length == 1){
                        var result = confirm("Are you sure? You have selected " + records.length + " record to delete.");
                    }
                    else{
                        var result = confirm("Are you sure? You have selected " + records.length + " records to delete.");
                    }
                    if(result){
                        $.ajax({
                            type : "post",
                            url : "/mastersheet/delete_selected/",

                            data : JSON.stringify({"records": records}),
                            contentType : "json",
                            success: function(response){
                                alert(response.response);


                            }

                        });
                    }
                }
            });

            $.each(columns_defs['buttons'], function(key,val){
                html_table = $("#example");
                html_table.find("thead>tr>th:eq("+val.slice(0,1)[0]+")").addClass("trFirst");
                $.each(val.slice(1,val.length-1),function(k,v){
                    html_table.find("thead>tr>th:eq("+v+")").addClass("trMiddle");
                });

                html_table.find("thead>tr>th:eq("+val.slice(val.length-1)[0]+")").addClass("trLast");
            });
            $("#buttons button")[0].click();
            $("#buttons button")[1].click();
            $("#buttons button")[2].click();
            $("#delete_selected").show();
        }

    }

    function select_rows(){
        //console.log("we are called...");
        $('#example tbody').on( 'click', 'tr', function () {
            $(this).toggleClass('selected');
            //console.log(this);
        });
    }

    $("#btnFetch").click(function(){
        load_data_datatable();
    });
    function flag_dates(){


        if( table != null){

            var data = table.rows({ page: 'current' }).data();
            var counter = 0;
            data.each(function (value, index) {
                counter = counter + 1;


                var p1 = new Date(Date.parse(value['phase_one_material_date_str'], "yyyy-mm-dd HH:mm:ss"));
                var p2 = new Date(Date.parse(value['phase_two_material_date_str'], "yyyy-mm-dd HH:mm:ss"));
                var p3 = new Date(Date.parse(value['phase_three_material_date_str'], "yyyy-mm-dd HH:mm:ss"));
                var a_d =  new Date(Date.parse(value['agreement_date_str'], "yyyy-mm-dd HH:mm:ss"));
                var s_t_d = new Date(Date.parse(value['septic_tank_date_str'], "yyyy-mm-dd HH:mm:ss"))
                var c_d = new Date(Date.parse(value['completion_date_str'], "yyyy-mm-dd HH:mm:ss"));

                //if (value['Household_number'] > 840){
                var ind = value['Household_number'] % 10;
                if(ind == 0){ind = 10;}

                if (value['agreement_date_str'] != null){

                    if ( value['phase_one_material_date_str'] == null && Math.floor((today - a_d) / divider) > 8 ){
                        //table.on("draw.dt", function(){
                            $('tr:eq('+ind+')').css('background-color', '#f9a4a4');//red
                       // });
                    }
                    else if ( value['phase_two_material_date_str'] == null && Math.floor((today - p1) / divider) > 8 ){
                        //table.on("draw.dt", function(){
                            $('tr:eq('+ind+')').css('background-color', '#f2f29f');//yellow
                        //});
                    }
                    else if (value['phase_three_material_date_str'] == null && Math.floor((today - p2) / divider) > 8 ){
                        //table.on("draw.dt", function(){
                            $('tr:eq('+ind+')').css('background-color', '#aaf9a4');//green
                       // });
                    }
                    else if (value['completion_date_str'] == null && Math.floor((today - p3) / divider) > 8 ){
                       // table.on("draw.dt", function(){
                            $('tr:eq('+ind+')').css('background-color', '#aaa4f4');//blue
                       //    });
                    }
                    /*if (value['phase_one_material_date_str'] - value['agreement_date_str'] > 8){

                    }*/
                }
                else{
                   $('tr:eq('+ind+')').css('background-color', '#adabab');//grey
                }



            });
            //console.log(counter);

        }
        else{
           console.log("table is null");
        }


    }

    $("#btnSync").click(function(){
        let slum = $("#slum_form").find('input[type=text]').val();
        if (slum!=""){
        $(".overlay").show();
        $.ajax({
            type : "get",
            url : "/mastersheet/sync/slum/"+slum,
            contentType : "json",
            success: function(response){
                $(".overlay").hide();
                alert(response.msg);
            },
            error : function(){
                $(".overlay").hide();
            }

        });
        }
        else{
            alert("Please select slum to sync.")
        }
    });

});

