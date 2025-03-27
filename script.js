const URI = "https://script.google.com/macros/s/AKfycbyDv1LS6Xo3F2EYN_wmJMGEyJ6BnjPp2v8ZuDrfGKWhO5fQpkktWsIYa7I6sqsoN4rh/exec";
let allData = [];

function fetchData(period) {
    $("#loading").show();
    fetch(`${URI}?period=${period}`)
        .then(response => response.json())
        .then(result => {
            if (result.status === "success") {
                $("#period").text(result.message.period);
                $("#startDate").text(new Date(result.message.metadata["start-date"]).toLocaleDateString());
                $("#endDate").text(new Date(result.message.metadata["end-date"]).toLocaleDateString());
                var remainingDays = Math.ceil((new Date(result.message.metadata["end-date"]) - new Date()) / (1000 * 60 * 60 * 24));
                $("#remainingDays").text(remainingDays);
                
                allData = result.message.data;
                
                let members = [...new Set(allData.map(item => item.member_name))];
                let memberOptions = "<option value='all'>All Members</option>";
                members.forEach(member => {
                    memberOptions += `<option value='${member}'>${member}</option>`;
                });
                $("#memberSelect").html(memberOptions);
                
                renderData();
            }
            $("#loading").hide();
        });
}

function renderData() {
    let selectedMember = $("#memberSelect").val();
    let filteredData = selectedMember === "all" ? allData : allData.filter(item => item.member_name === selectedMember);
    
    let doneCount = 0, inProgressCount = 0, todoCount = 0;
    let totalCount = filteredData.length;
    let dataHtml = "";

    filteredData.forEach(item => {
        let alertClass = "alert-secondary";
        if (item.status === "done") {
            alertClass = "alert-success";
            status = "Done";
            icon = "far fa-circle-check";
            doneCount++;
        } else if (item.status === "in_progress") {
            alertClass = "alert-primary";
            status = "In Progress";
            icon = "far fa-hourglass";
            inProgressCount++;
        } else {
            alertClass = "alert-light";
            status = "Todo";
            icon = "fas fa-list-ul";
            todoCount++;
        }
        
        dataHtml += `
            <div class="col-md-4">
                <div class="shadow bg-body-tertiary rounded">
                    <div class="alert ${alertClass} p-3 mb-3" data-juz="${item.juz}" data-member="${item.member_name}" data-status="${item.status}" onclick="openModal(this)">
                        <div class="row align-items-center">
                            <div class="col-2 d-flex flex-column align-items-center justify-content-center">
                                <h5 class="mb-1">Juz</h5>
                                <h1 class="mb-0">${item.juz}</h1>
                            </div>
                            
                            <div class="col-7 d-flex flex-column">
                                <h4 class="mb-1">${item.member_name}</h4>
                                <p class="mb-0">${status}</p>
                            </div>

                            <div class="col-3 d-flex justify-content-center">
                                <i class="${icon} display-6"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    
    $("#data-container").html(dataHtml);
    
    let donePercentage = totalCount > 0 ? (doneCount / totalCount * 100).toFixed(1) + "%" : "0%";
    let inProgressPercentage = totalCount > 0 ? (inProgressCount / totalCount * 100).toFixed(1) + "%" : "0%";
    let todoPercentage = totalCount > 0 ? (todoCount / totalCount * 100).toFixed(1) + "%" : "0%";
    
    $("#progressDone").css("width", donePercentage).text("Done: " + donePercentage);
    $("#progressInProgress").css("width", inProgressPercentage).text("In Progress: " + inProgressPercentage);
    $("#progressTodo").css("width", todoPercentage).text("Todo: " + todoPercentage);
}


function openModal(element) {
    let juz = $(element).data("juz");
    let member = $(element).data("member");
    let status = $(element).data("status");
    $("#modalJuz").val(juz);
    $("#modalJuzDisplay").text(juz);
    $("#modalMember").val(member);
    $("#modalStatus").val(status);
    $("#statusModal").modal("show");
}

function saveStatus(button) {
    let juz = parseInt($("#modalJuz").val());
    let member = $("#modalMember").val();
    let status = $("#modalStatus").val();
    $("#loading").show();
    fetch(`${URI}`, {
        method: "POST",
        mode: "no-cors", 
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({
            juz: juz,
            member_name: member,
            status: status,
            period: "current"
        })
    }).then(() => {
        fetchData("current");
    });
}

$(document).ready(function() {
    $("#loading").show();
    fetch(`${URI}?period=current`)
        .then(response => response.json())
        .then(result => {
            if (result.status === "success") {
                let periods = result.message.periods;
                let periodSelect = "";
                periods.forEach(p => {
                    periodSelect += `<option value="${p}">${p}</option>`;
                });
                $("#periodSelect").html(periodSelect);
                
                fetchData(result.message.period);
            }
        });
    
    $("#periodSelect").on("change", function() {
        fetchData($(this).val());
    });
    
    $("#memberSelect").on("change", function() {
        renderData();
    });
});