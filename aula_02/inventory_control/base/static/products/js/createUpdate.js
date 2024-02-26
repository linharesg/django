jQuery(function() {
    const $addButton = $("#addSupplierButton");
    const $suppliersContainer = $("#supplierFormset");
    const $totalSuppliers = $("#id_supplierproduct_set-TOTAL_FORMS")
    const $initialSuppliers = $("#id_supplierproduct_set-INITIAL_FORMS")
    
    console.log($totalSuppliers)

    const $originalSupplier = $suppliersContainer.children(".row:first").clone(true);

    const updateFormIndex = function(){
        $(".productRow").each(function(index) {
            $(this).find(":input, select, label, div").each(function() {
                const name = $(this).attr("name")
                const id = $(this).attr("id")
                if (name) {
                    const newName = name.replace(/-\d-/, `-${index}-`)
                    $(this).attr("name", newName)

                }
                if (id) {
                    const newId = id.replace(/-\d-/, `-${index}-`)
                    $(this).attr("id", newId)
                }
            })

        })
    }

    $addButton.on("click", function(){
        const $newRow = $originalSupplier.clone(true);
        const index = parseInt($totalSuppliers.val());
        console.log(index)
        $newRow.find(":input[name]").each(function() {
            const name = $(this).attr("name").replace("-0-", `-${index}-`)
            const id = "id_" + name;

            $(this).attr({ name, id }).val("");
            $(this).find('option').removeAttr('selected');
        });

        $newRow.find("div>div[id]").each(function() {
            console.log("2")
            const id = $(this).attr("id").replace("-0-", `-${index}-`)
            // console.log(id)
            // console.log($(this))
            $(this).attr({ id }).val("");
            // console.log($(this))
        });

        $newRow.find("button[data-url").each(function() {
            console.log("3")
            const oldUrl = $(this).attr("data-url");
            const newUrl = oldUrl.replace(/\d+/, '0');
            $(this).attr("data-url", newUrl).val("");
        });

        $totalSuppliers.val(index + 1);
        $suppliersContainer.append($newRow);
    });

    $suppliersContainer.on("click", ".remove-btn", function() {
        const $button = $(this);

        $button.closest(".row").remove();
        $totalSuppliers.val(parseInt($totalSuppliers.val()) -1);
        
        if (parseInt($initialSuppliers.val()) > 0) {
            $initialSuppliers.val(parseInt($initialSuppliers.val()) -1);
            updateFormIndex()
        };
        const url = $button.data("url");
        if (url) {
            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": Cookies.get("csrftoken")
                }
            })
            .catch(console.error);
        }

    });

});