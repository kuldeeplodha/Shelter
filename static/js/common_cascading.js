
function cityList(){
    $.ajax({
        url : city_url,
        //data : {},
        type: "GET",
        contenttype : "json",
        success : function(json){
            var str='<option value="';
            str = str +"0" +'"'+'>' + "---select---" + '</option>';
            $('#id_City').append(str);
            for (i = 0; i < json.nameArray.length; i++){
              var str='<option value="';
              str = str +json.idArray[i] +'"'+'>' + json.nameArray[i] + '</option>';
              $('#id_City').append(str);
           }
           slumid=$('#id_slum_name').val();
      		 if(slumid)
      		 {
          		filllist();
      	 	}
        },
        sync:false
    });
}

function administrativewardList(){
    $('#id_AdministrativeWard').empty();
    var cityname = $("#id_City option:selected").text();
    var id = $("#id_City option:selected").val();
    $.ajax({
        url : administrative_url,
        data : { id : id},
        type: "POST",
        contenttype : "json",
        success : function(json){
              var str='<option value="';
              str = str +"0" +'"'+'>' + "---select---" + '</option>';
              $('#id_AdministrativeWard').append(str);
        for (i = 0; i < json.nameArray.length; i++){
                var str='<option value="';
                str = str +json.idArray[i] +'"'+'>' + json.nameArray[i] + '</option>';
                $('#id_AdministrativeWard').append(str);
            }
        },
        async:false
    });
}

function electoralWardList(){
    $('#id_ElectoralWard').empty();
    var Administrativewardname = $("#id_AdministrativeWard option:selected").text();
    var id = $("#id_AdministrativeWard option:selected").val();

    $.ajax({
        url : electoral_url,
        data : { id : id},
        type: "POST",
        contenttype : "json",
        success : function(json){
            var str='<option value="';
              str = str +"0" +'"'+'>' + "---select---" + '</option>';
            $('#id_ElectoralWard').append(str);
        for (i = 0; i < json.nameArray.length; i++) {
            var str='<option value="';
            str = str +json.idArray[i] +'"'+'>' + json.nameArray[i] + '</option>';
            $('#id_ElectoralWard').append(str);
        }
        },
        async:false
    });
}
function slumList(){
    $('#id_slum_name').empty();
    var Administrativewardname = $("#id_ElectoralWard option:selected").text();
    var id = $("#id_ElectoralWard option:selected").val();

    $.ajax({
        url : slum_url,
        data : { id : id},
        type: "POST",
        contenttype : "json",
        success : function(json){
          var str='<option value="';
          str = str +"0" +'"'+'>' + "---select---" + '</option>';
          $('#id_slum_name').append(str);
        for (i = 0; i < json.nameArray.length; i++) {
            var str='<option value="';
            str = str +json.idArray[i] +'"'+'>' + json.nameArray[i] + '</option>';
            $('#id_slum_name').append(str);
            }
        },
        async:false
    });

}

function filllist(){
    var id = $('#id_slum_name').val();
    var url = "{% url 'modelList' %}";

    $.ajax({
        url : url,
        data : { id : id },
        type: "POST",
        contenttype : "json",
        success :function(json){
           var a=json.cid;
           $("#id_City option[value='"+json.cid+"']").attr("selected", "selected");
            administrativewardList();
            $("#id_AdministrativeWard option:selected").val(json.aid);
            $("#id_AdministrativeWard option:selected").text(json.aname);
            electoralWardList();
            $("id_ElectoralWard option[value='"+json.eid+"']").attr("selected", "selected");
            $("#id_ElectoralWard option:selected").val(json.eid);
            $("#id_ElectoralWard option:selected").text(json.ename);
             slumList();
            $("#id_slum_name option:selected").val(json.sid);
            $("#id_slum_name option:selected").text(json.sname);
        },
        async:false
    });
}

$(document).ready(function(){

	 $("#AdministrativeWards").hide();
   $("#ElectoralWards").hide();
   $("#Slums").hide();

	 slumid=$('#id_slum_name').val();
   if(slumid)
   {
       $("#AdministrativeWards").show();
   	   $("#ElectoralWards").show();
       $("#Slums").show();
    }

    cityList();

    $("#id_City").on('change',function()
    {
        $("#AdministrativeWards").show();
        $("#ElectoralWards").hide();
        $("#Slums").hide();
       	administrativewardList();
    });

    $("#id_AdministrativeWard").on('change',function()
    {
        $("#ElectoralWards").show();
        $("#Slums").hide();
        electoralWardList();
    });

    $("#id_ElectoralWard").on('change',function()
    {
        $("#Slums").show();
         slumList();
    });

});
