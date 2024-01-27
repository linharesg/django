// jQuery(function() {
//     const $enabledCheckbox = $(".form-check-input")

//     $enabledCheckbox.on("click", function() {
//         const url = $(this).data("url");
        
//         console.log(url);
//         console.log("oi")
//         console.log($enabledCheckbox)
//         console.log("oi")
//         console.log($(this))

//         fetch(url, {
//             method: "POST",
//             headers: {
//                 "X-CSRFToken": Cookies.get("csrftoken")
//             }
//         })
//         .then(res => res.json())
//         .then(data => console.log(data))
//         .catch(console.error);
//     });
// });