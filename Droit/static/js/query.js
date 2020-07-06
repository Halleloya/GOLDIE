
const jsonFormatter = new JSONFormatter("json-thingdescription", false)
const $tdModal = $("#thing_description_modal");

// Register click event for each thing description items in the result table
$(".result table tbody").on("click", "button", function () {
    let thingDescription = $(this).siblings('div').text().trim();
    jsonFormatter.setJSONString(thingDescription);
    $tdModal.modal('show');
});


// Register click event for the 'search' button
$("#search").click(function () {
    let form_data = $(".register-form").serialize();
    let request_url = `${SEARCH_API}?${form_data}`

    /** Send asynchronous request to delete the thing description */
    let $resultContainer = $('.result');

    $resultContainer.hide();
    lock_btn($(this));
    fetch(request_url)
        .then(response => response.json())
        .then(data => {
            // Show result list 
            $resultContainer.show();
            // render each thing description
            $tableBody = $(".result table tbody");
            $tableBody.html("");
            data.forEach(element => {
                $tableBody.append(`<tr>
                <td>${element.thing_id}</td>
                <td>${element.thing_type}</td>
                <td>${element.title}</td>
                <td>
                    <button class="btn btn-primary">Show</button>
                    <div hidden>
                        ${JSON.stringify(element)}
                    </div>
                </td>
                </tr>`);
            });

            unlock_btn($(this));
        })
        .catch(response => {
            show_prompt('Search failed, please try again using valid input');
            unlock_btn($(this));
        });
});