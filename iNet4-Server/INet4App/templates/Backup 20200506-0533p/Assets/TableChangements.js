var csrftoken = $.cookie('csrftoken');
var RefreshSeconds = 60;


let theEditor;

ClassicEditor.create( document.querySelector( '#editor1' ) )
    .then( editor => {
        theEditor = editor;
    })
    .catch( error => {
        console.error( error );
    } );


function getDataFromTheEditor() {
    return theEditor.getData();
}

function FileStatusName(ex){
    switch(ex) {
          case 't':
            return "InTrans"
            break;
          case 'e':
            return "InQueue"
            break;
          case 'c':
            return "Completed"
            break;
          case 'a':
            return "Archived"
            break;
          case 'h':
            return "Hibernate"
            break;
          case 's':
            return "Saved"
            break;
          default:
            return "Unknown"
        }
}

function UpdateJobsContent(result){
        var obj = JSON.parse(result);
        if(result.length > 0)
        {
           content = '';
           var count = 0;
        for(var k in obj)
        {
            count++;
            if (obj[k]["Marked"] == "1")
                content += "<tr class='table-row bg-success'>"
            else if (obj[k]["DragonTranscribedText"] != "" && obj[k]["Priority"] != 'P')
                content += "<tr class='table-row bg-primary'>"
            else if(obj[k]["Priority"] == 'P' && obj[k]["DragonTranscribedText"] != "")
                content += "<tr class='table-row table-danger'>"
            else if(obj[k]["Priority"] == 'P' && obj[k]["DragonTranscribedText"] == "")
                content += "<tr class='table-row bg-danger'>"
            else
                content += "<tr class='table-row'>"

            content += '<td class="Jnom">'+ obj[k]["JobNumber"] + '</td>';
            content += '<td>'+ FileStatusName(obj[k]["FileStatus"]) + '</td>';
            content += '<td>'+ obj[k]["AuthorNameLast"] + '</td>';
            content += '<td>'+ obj[k]["Secretary"] + '</td>';
            content += '<td>'+ obj[k]["Subject"] + '</td>';
            content += '<td>'+ obj[k]["Worktype"] + '</td>';
            content += '<td>'+ obj[k]["Length"] + '</td>';
            content += '<td>'+ obj[k]["DateDictation"] + '</td>';
            content += '<td>'+ obj[k]["TimeDictation"] + '</td>';
            content += '<td>'+ obj[k]["Department"] + '</td>';
            content += '<td>'+ obj[k]["TransNameLast"] + '</td>';
            content += '<td>'+ obj[k]["DateTranscription"] + '</td>';
            content += '<td>'+ obj[k]["TimeTranscription"] + '</td>';
            content += '<td class="Fname" hidden>'+ obj[k]["subFname"]+'</td>';
            content += '<td>'+ obj[k]["Priority"] + '</td>';
            content += '<td>'+ obj[k]["SystemId"] + '</td>';
            content += '<td>'+ obj[k]["Location"] + '</td>';
            content += '<td class="DTT" hidden>'+ obj[k]["DragonTranscribedText"] + '</td>';
            content += '<td>'+ obj[k]["Marked"] + '</td>';
        }
        document.getElementById('RowCount').innerHTML = count;
        $('#TBchange tbody').html(content);
        }
}

function refreshPage(){
        var st = document.getElementById('SelectedStatus').value;
        var ex = document.getElementById('SelectedExclusive').value;
        var au = document.getElementById('AutherInput').value;
        var wt = document.getElementById('WorktypeInput').value;
        var dp = document.getElementById('DeptInput').value;
        var AID = document.getElementById('Auth_id').textContent;
        $.ajax({
              type: 'POST',
              url: listJobURL,
              data: {
                 AutherInput: au,
                 WorktypeInput: wt,
                 DeptInput: dp,
                 SelectedStatus: st,
                 SelectedExclusive: ex,
                 AuthID: AID,
                 csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success: function(result){
                   UpdateJobsContent(result);
               },
              error: function (response) {
                    console.log("Error: " + response);
                }
        });
}

function SaveJob(){
        var Jnom = document.getElementById('SelectedJobID').textContent;
        var AuID = document.getElementById('Auth_id').textContent;
        var st = document.getElementById('SelectedStatus').value;
        var ex = document.getElementById('SelectedExclusive').value;
        var au = document.getElementById('AutherInput').value;
        var wt = document.getElementById('WorktypeInput').value;
        var dp = document.getElementById('DeptInput').value;
        var Audioduration = document.getElementById('AudioBLC').currentTime;
        if(!document.getElementById('AudioBLC').paused){
            document.getElementById('AudioBLC').pause();
        }
        //console.log("Jnom: " + Jnom);
        //console.log("saved on min: " + Audioduration);

        if (Jnom == "" || Jnom == undefined)
        {
            alert("Nothing here man");
            return;
        }
        console.log("Auth ID: " + AuID);
        $.ajax({
          type: 'POST',
          url: SaveJobURL,
          data: {
              jnom : Jnom,
              AuID : AuID,
              SelectedStatus : st,
              SelectedExclusive : ex,
              AutherInput : au,
              WorktypeInput : wt,
              DeptInput : dp,
              Audioduration : Audioduration,
             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          },
          success: function(result){
              UpdateJobsContent(result);
              document.getElementById("JobDetailDIV").style.display = "none";
              //document.getElementById("FormCollapse").style.display = "none";
              document.getElementById('job_detail').innerText = "";
           },
          error: function (response) {
            console.log(" T-T ");
            }
    });
}

$(document).ready(function(){
        document.getElementById("JobDetailDIV").style.display = "none";
        setTimeout(refreshPage, RefreshSeconds*1000);
        // document.getElementById("JobDetailDIV").style.display = "none";
        $("#AutherInput").on("input", function(e){
                e.preventDefault();
                var st = document.getElementById('SelectedStatus').value;
                var ex = document.getElementById('SelectedExclusive').value;
                var au = document.getElementById('AutherInput').value;
                var wt = document.getElementById('WorktypeInput').value;
                var dp = document.getElementById('DeptInput').value;
                var AID = document.getElementById('Auth_id').textContent;
                //console.log("ID:" + AID);
                WorktypeInput
                $.ajax({
                  type: 'POST',
                  url: listJobURL,
                  data: {
                     AutherInput: au,
                     WorktypeInput: wt,
                     DeptInput: dp,
                     SelectedStatus: st,
                     SelectedExclusive: ex,
                     AuthID: AID,
                     csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                  },
                  success: function(result){
                       UpdateJobsContent(result);
                   },
                  error: function (response) {
                        console.log("Error: " + response);
                    }
                });
            });

        $("#WorktypeInput").on("input", function(e){
                e.preventDefault();
                var st = document.getElementById('SelectedStatus').value;
                var ex = document.getElementById('SelectedExclusive').value;
                var au = document.getElementById('AutherInput').value;
                var wt = document.getElementById('WorktypeInput').value;
                var dp = document.getElementById('DeptInput').value;
                var AID = document.getElementById('Auth_id').textContent;
                $.ajax({
                  type: 'POST',
                  url: listJobURL,
                  data: {
                     AutherInput: au,
                     WorktypeInput: wt,
                     DeptInput: dp,
                     SelectedStatus: st,
                     SelectedExclusive: ex,
                     AuthID: AID,
                     csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                  },
                  success: function(result){
                   UpdateJobsContent(result);
                   },
                  error: function (response) {
                        console.log("Error: " + response);
                    }
                });
            });

        $("#DeptInput").on("input", function(e){
                e.preventDefault();
                var st = document.getElementById('SelectedStatus').value;
                var ex = document.getElementById('SelectedExclusive').value;
                var au = document.getElementById('AutherInput').value;
                var wt = document.getElementById('WorktypeInput').value;
                var dp = document.getElementById('DeptInput').value;
                var AID = document.getElementById('Auth_id').textContent;
                $.ajax({
                  type: 'POST',
                  url: listJobURL,
                  data: {
                     AutherInput: au,
                     WorktypeInput: wt,
                     DeptInput: dp,
                     SelectedStatus: st,
                     SelectedExclusive: ex,
                     AuthID: AID,
                     csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                  },
                  success: function(result){
                    UpdateJobsContent(result);
                   },
                  error: function (response) {
                        console.log("Error: " + response);
                    }
                });
        });


        $("#SelectedStatus").change(function (e){
                e.preventDefault();
                var st = document.getElementById('SelectedStatus').value;
                var ex = document.getElementById('SelectedExclusive').value;
                var au = document.getElementById('AutherInput').value;
                var wt = document.getElementById('WorktypeInput').value;
                var dp = document.getElementById('DeptInput').value;
                var AID = document.getElementById('Auth_id').textContent;
                $.ajax({
                  type: 'POST',
                  url: listJobURL,
                  data: {
                     AutherInput: au,
                     WorktypeInput: wt,
                     DeptInput: dp,
                     SelectedStatus: st,
                     SelectedExclusive: ex,
                     AuthID: AID,
                     csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                  },
                  success: function(result){
                    UpdateJobsContent(result);
                   },
                  error: function (response) {
                        console.log("Error: " + response);
                    }
                });
        });

        $("#SelectedExclusive").change(function (e){
                e.preventDefault();
                var st = document.getElementById('SelectedStatus').value;
                var ex = document.getElementById('SelectedExclusive').value;
                var au = document.getElementById('AutherInput').value;
                var wt = document.getElementById('WorktypeInput').value;
                var dp = document.getElementById('DeptInput').value;
                var AID = document.getElementById('Auth_id').textContent;
                //console.log("ID:" + AID);
                $.ajax({
                  type: 'POST',
                  url: listJobURL,
                  data: {
                     AutherInput: au,
                     WorktypeInput: wt,
                     DeptInput: dp,
                     SelectedStatus: st,
                     SelectedExclusive: ex,
                     AuthID: AID,
                     csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                  },
                  success: function(result){
                    UpdateJobsContent(result);
                   },
                  error: function (response) {
                        console.log("Error: " + response);
                    }
                });
        });
    });

function scrollToTop() {
            $(window).scrollTop(0);
        }

$(document).on("click", "tbody tr", function() {
            var JDetail = document.getElementById('job_detail').textContent;
            console.log(JDetail)
            if (JDetail != "" && JDetail != undefined)
            {
                alert("Please return your existing job before requesting another");
                return;
            }
            var filenameID = $(this).closest('tr').find('.Fname').text();
            filename = "https://dictationportal.com:4445/Files/" + filenameID;
            var audio = document.getElementById('AudioBLC');
            var Jnom = document.getElementById('SelectedJobID').textContent;
            var AuID = document.getElementById('Auth_id').textContent;
            var st = document.getElementById('SelectedStatus').value;
            var ex = document.getElementById('SelectedExclusive').value;
            var au = document.getElementById('AutherInput').value;
            var wt = document.getElementById('WorktypeInput').value;
            var dp = document.getElementById('DeptInput').value;
            var SJID = document.getElementById('SelectedJobID');
            var DTT = $(this).closest('tr').find('.DTT').text();
            var editor1 = document.getElementById('editor1');
            SJID.innerHTML = $(this).closest('tr').find('.Jnom').text();
            //($(this).closest('tr').find('.Jnom').text());
            var source = document.getElementById('audSRC');
            //added labels for versatility
            var SysSub = document.getElementById('SysSub').textContent;
            var SysWT = document.getElementById('SysWT').textContent;
            var SysDept = document.getElementById('SysDept').textContent;
            var SysTyp = document.getElementById('SysTyp').textContent;

            var JSub = $(this).closest('tr').find('.JSub').text();
            var JWT = $(this).closest('tr').find('.JWT').text();
            var JDept = $(this).closest('tr').find('.JDept').text();
            var JPri = $(this).closest('tr').find('.JPri').text();
            var JDate = $(this).closest('tr').find('.JDate').text();
            var JTime = $(this).closest('tr').find('.JTime').text();
            var JAuth = $(this).closest('tr').find('.JAuth').text();
            //+ "  " + SysSub + ":  "+JSub
            //source.src = none;
          $.ajax({
              type: 'POST',
              url: SignjoboutURL,
              data: {
                  SJID : SJID.textContent,
                  AuID : AuID,
                  SelectedStatus : st,
                  SelectedExclusive : ex,
                  AutherInput : au,
                  WorktypeInput : wt,
                  DeptInput : dp,
                 csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success: function(result){
                  console.log(result)
                var r1 = result.substr(0, result.indexOf(']')+1);
                var r1 = result.substr(0, result.indexOf(']')+1);
                var r2 = result.substring(r1.length,result.length);
                var DTT_P1 = DTT.substr(0,DTT.indexOf('@@@'));

                var DTT_P2 = DTT.substr(DTT_P1.length + 3,DTT.length);
                var DTTp2 = DTT_P2.split("@@@").join("<br/>");
                console.log("P1:"+ DTT_P1);
                console.log("P2:"+ DTT_P2);
                console.log("P2.5:"+ DTTp2);
                UpdateJobsContent(r2);
                source.src = filename;
                audio.load();
                audio.currentTime = JSON.parse(r1)[0]["SavedOffset"];
                document.getElementById("JobDetailDIV").style.display = "Block";
                theEditor.setData(DTTp2);
                theEditor.updateSourceElement();

                // document.getElementById("FormCollapse").style.display = "Block";
                // if (DTTp2 != "" || DTTp2 != undefined) {
                //     document.getElementById("FormCollapse").style.display = "Block";
                // }

                document.getElementById('job_detail').innerText = "      Job " + SJID.textContent + "   " +  JAuth + "   " + SysSub + ": "+JSub+ "    " + SysWT + ": "+JWT+ "    " + SysDept + ": "+JDept;
                scrollToTop();
                //   var res = result.split("|");
                // var r2 = res[1];
                // var r3 = res[2];
                // var r4= res[3];
                //
                // let r5 = toString(r3.value)
                // console.log("r1: " + r1);
                // //console.log("r2: " + r2);
                // console.log(r3);
                // console.log(r4);
                //
                // document.getElementById('job_detail').innerText = "      JobNumber " + SJID.textContent + "      ";
                // // document.getElementById('job_detail1').innerText = r1.value;
                //
                // // job_detail
                // var DTT_P1 = DTT.substr(0,DTT.indexOf('@@@'));
                //
                // var DTT_P2 = DTT.substr(DTT_P1.length + 3,DTT.length);
                // var DTTp2 = DTT_P2.split("@@@").join("<br/>");
                // console.log("P1:"+ DTT_P1);
                // console.log("P2:"+ DTT_P2);
                // console.log("P2.5:"+ DTTp2);
                // UpdateJobsContent(r2);
                // source.src = filename;
                // audio.load();
                // audio.currentTime = JSON.parse(r1)[0]["SavedOffset"];
                // document.getElementById("JobDetailDIV").style.display = "Block";
                // theEditor.setData(DTTp2);
                // theEditor.updateSourceElement();

               },
              error: function (response) {
                console.log(" T-T ");
                }
        });
            //console.log("val: " + SJID.textContent);
          //alert("clicked: " + filenameID);
  });

function ReturnJob(){
        var Jnom = document.getElementById('SelectedJobID').textContent;
        var AuID = document.getElementById('Auth_id').textContent;
        var st = document.getElementById('SelectedStatus').value;
        var ex = document.getElementById('SelectedExclusive').value;
        var au = document.getElementById('AutherInput').value;
        var wt = document.getElementById('WorktypeInput').value;
        var dp = document.getElementById('DeptInput').value;
        //console.log("Jnom: " + Jnom);
        if (Jnom == "" || Jnom == undefined)
        {
            alert("Nothing here man");
            return;
        }
        //console.log("Auth ID: " + AuID);
        $.ajax({
          type: 'POST',
          url: ReturnJobURL,
          data: {
              jnom : Jnom,
              AuID : AuID,
              SelectedStatus : st,
              SelectedExclusive : ex,
              AutherInput : au,
              WorktypeInput : wt,
              DeptInput : dp,
             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          },
          success: function(result){
              UpdateJobsContent(result);
              document.getElementById("JobDetailDIV").style.display = "none";
              //document.getElementById("FormCollapse").style.display = "none";
              document.getElementById('job_detail').innerText = "";
           },
          error: function (response) {
            //console.log(" T-T ");
            }
    });
}

function completeJob(){
            var Jnom = document.getElementById('SelectedJobID').textContent;
            var AuID = document.getElementById('Auth_id').textContent;
            var st = document.getElementById('SelectedStatus').value;
            var ex = document.getElementById('SelectedExclusive').value;
            var au = document.getElementById('AutherInput').value;
            var wt = document.getElementById('WorktypeInput').value;
            var dp = document.getElementById('DeptInput').value;
            console.log("Jnom: " + Jnom);
            if (Jnom == "" || Jnom == undefined)
            {
                alert("Nothing here man");
                return;
            }
            console.log("Auth ID: " + AuID);
            $.ajax({
              type: 'POST',
              url: CompleteJobURL,
              data: {
                  jnom : Jnom,
                  AuID : AuID,
                  SelectedStatus : st,
                  SelectedExclusive : ex,
                  AutherInput : au,
                  WorktypeInput : wt,
                  DeptInput : dp,
                  csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success: function(result){
                UpdateJobsContent(result);
                document.getElementById("JobDetailDIV").style.display = "none";
                //document.getElementById("FormCollapse").style.display = "none";
                document.getElementById('job_detail').innerText = "";
               },
              error: function (response) {
                console.log(" T-T ");
               }
        });

}
