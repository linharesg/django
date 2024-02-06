jQuery(function() {
    $("#submitButton").on("click", function() {
        $button = $(this);

        $button.prop("disabled", true);

        $("#buttonText").text("Carregando...")
        $("#loadingSpinner").show();

        $("form").submit();
    })
})