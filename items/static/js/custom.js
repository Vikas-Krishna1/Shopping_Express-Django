$(document).ready(function () {
   $(document).on("change", 'select[name^="quantity_"]', function () {
    const qty = Number($(this).val());

    // extract item id from name="quantity_12"
    const itemId = $(this).attr("name").replace("quantity_", "");

    console.log("qty changed", itemId, qty);

    const checkbox = $('input[name="selected_items"][value="' + itemId + '"]');

    checkbox.prop("checked", qty > 0);
  });

  // Checkbox unchecked → reset quantity to 0
  $(document).on("change", 'input[name="selected_items"]', function () {
    const itemId = $(this).val();

    console.log("checkbox changed", itemId, this.checked);

    if (!this.checked) {
      $('select[name="quantity_' + itemId + '"]').val("0");
    }
  });

  // Disable clear button if cart is empty
  const $clearBtn = $('button[name="action"][value="clear"]');

  function updateClearButton() {
    const cartHasItems = $(".cart-summary-section tbody tr").length > 0;
    $clearBtn.prop("disabled", !cartHasItems);
  }

  // Initial state
  updateClearButton();

  // Add / Remove validation
  $(document).on("submit", "form", function (e) {
    const action = $(document.activeElement).val();
    if (!["add", "remove", "clear"].includes(action)) return;

    const checkedCount = $('input[name="selected_items"]:checked').length;

    // ADD
    if (action === "add" && checkedCount === 0) {
      e.preventDefault();
      alert("Select at least one item by choosing a quantity greater than 0.");
    }

    // REMOVE
    if (action === "remove" && checkedCount === 0) {
      e.preventDefault();
      alert("Select at least one item to remove.");
    }

    // CLEAR
    if (action === "clear") {
      const cartHasItems = $(".cart-summary-section tbody tr").length > 0;
      if (!cartHasItems) {
        e.preventDefault();
        alert("Your cart is already empty.");
      }
    }
  });

  // Re-evaluate Clear button after page changes
  $(document).on("change", "select[name^='quantity_'], input[name='selected_items']", function () {
    updateClearButton();
  });
});
