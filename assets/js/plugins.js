import * as Turbo from "@hotwired/turbo";
import Tagify from "@yaireo/tagify";
import { Toast } from "bootstrap";
import feather from "feather-icons";
import flatpickr from "flatpickr";
import IMask from "imask";
import Cookies from "js-cookie";
import Swal from "sweetalert2";
import "trix";

/**
 * Initialize all JavaScript plugins.
 */
export function initializePlugins() {
  // Bootstrap
  document.querySelectorAll(".toast").forEach(initializeBootstrapToast);

  // Feather Icons
  initializeFeatherIcons();

  // Flatpickr
  initializeFlatpickr();

  // Tagify
  document.querySelectorAll("input.tagsinput").forEach(initializeTagify);

  // IMask
  document
    .querySelectorAll("input.moneyinput")
    .forEach(initializeMoneyInputMask);

  // Trix
  document.addEventListener("trix-attachment-add", handleTrixAttachment);

  // SweetAlert2
  document
    .querySelectorAll("button[data-confirm-submit]")
    .forEach((el) => el.addEventListener("click", handleActionButton));

  // DataTable
  document.querySelectorAll("form[data-table]").forEach(initializeDataTable);
}

/**
 * Display all feather icons.
 */
function initializeFeatherIcons() {
  feather.replace({ width: "1em", height: "1em", "stroke-width": 2 });
}

/**
 * Enable flatpickr plugin for date and datetime inputs.
 */
function initializeFlatpickr() {
  // Date input
  flatpickr("input.dateinput", {
    enableTime: false,
    altInput: true,
    altFormat: "F j, Y",
    dateFormat: "Y-m-d",
  });

  // Datetime input
  flatpickr("input.datetimeinput", {
    enableTime: true,
    altInput: true,
    altFormat: "F j, Y H:i",
    dateFormat: "Z", // Use ISO 8601 to make it timezone aware in Django.
  });
}

/**
 * Show the bootstrap toast for displaying the notifications from Django
 * messages framework.
 *
 * @param {HTMLElement} element the tost container element
 */
function initializeBootstrapToast(element) {
  new Toast(element).show();
}

/**
 * Initialize the data table element from the DataTableView.
 *
 * Make sure when the user select or deselect all item checkbox in the table
 * heading, all checkboxes in table changed accordingly.
 *
 * @param {HTMLElement} element the data table form element
 */
function initializeDataTable(element) {
  // When the user select or deselect all item checkbox in the table heading,
  // all checkboxes in table changed accordingly.
  element
    .querySelector("input[data-table-select-all]")
    .addEventListener("change", function (event) {
      element
        .querySelectorAll("input[data-table-select-item]")
        .forEach((item) => (item.checked = event.target.checked));
    });

  // When the user change how much entries to display per page, change the URL
  // search params, which will refetch the page.
  element
    .querySelector('select[name="per_page"]')
    .addEventListener("change", function (event) {
      const url = new URL(window.location.href);
      url.searchParams.set("per_page", event.target.value);
      Turbo.visit(url.href, { action: "replace" });
    });
}
/**
 * Initialize the Tagify plugin for multi-tags input.
 *
 * Make sure that the form value is joined with comma separator, so that Django
 * can handle it.
 *
 * @param {HTMLElement} element the tagify text input element
 */
function initializeTagify(element) {
  new Tagify(element, {
    originalInputValueFormat: (values) =>
      values.map((item) => item.value).join(","),
  });
}

/**
 * Initialize the IMask plugin for currency/price form inputs.
 *
 * @param {HTMLElement} element the text input element
 */
function initializeMoneyInputMask(element) {
  // Create the mask for currency inputs.
  const mask = IMask(element, {
    mask: Number,
    thousandsSeparator: ",",
    scale: 2,
    radix: ".",
  });

  // When the user submits the form, replace the value to the original value,
  // without the comma separator.
  element.form.addEventListener("submit", function (event) {
    element.value = mask.unmaskedValue;
  });
}

/**
 * Transform a button to an "action button".
 *
 * A SweetAlert2 confirmation popup will be shown if the user clicked the
 * button. If the user click "Confirm", an HTML form will be created in the
 * document body and submitted to the given URL.
 *
 * @param {MouseEvent} event the button click event
 */
async function handleActionButton(event) {
  // Collect the action button data from the element `data-*` attributes.
  const url = event.target.getAttribute("data-confirm-submit");
  const title = event.target.getAttribute("data-title");
  const description = event.target.getAttribute("data-description");
  const confirmTitle = event.target.getAttribute("data-confirm-title");
  const confirmColor = event.target.getAttribute("data-confirm-color");
  const rejectTitle = event.target.getAttribute("data-reject-title");
  const rejectColor = event.target.getAttribute("data-reject-color");

  // Display the confirmation popup.
  const result = await Swal.fire({
    icon: "warning",
    title: title ?? "Are you sure?",
    html: description ?? "You won't be able to revert this!",
    showCancelButton: true,
    buttonsStyling: false,
    confirmButtonText: confirmTitle ?? "Delete",
    cancelButtonText: rejectTitle ?? "Cancel",
    customClass: {
      confirmButton: `btn btn-${confirmColor ?? "danger"}`,
      cancelButton: `btn btn-${rejectColor ?? "secondary"} ms-3`,
    },
  });

  // Handle when the user clicked "Confirm" button.
  if (result.isConfirmed) {
    // Create a form element.
    const formElement = document.createElement("form");
    formElement.setAttribute("method", "POST");
    formElement.setAttribute("action", url);

    // Attach the CSRF token value to the form that we get from the cookies
    // to prevent 403 forbidden error.
    const csrfElement = document.createElement("input");
    csrfElement.setAttribute("type", "hidden");
    csrfElement.setAttribute("name", "csrfmiddlewaretoken");
    csrfElement.setAttribute("value", Cookies.get("csrftoken"));

    // Attach the form element to the HTML body so that we can call `submit`
    // programatically. Otherwise, it will throw an error.
    formElement.appendChild(csrfElement);
    document.body.appendChild(formElement);

    // Submit the form.
    formElement.submit();
  }
}

/**
 * Handle when the user upload an image to the Trix editor.
 *
 * @param {*} event the trix upload attachment event
 */
function handleTrixAttachment(event) {
  const { attachment } = event;

  if (attachment.file) {
    // Store the image to a form data.
    const formData = new FormData();
    formData.append("file", event.attachment.file);

    // Initialize
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload-media/", true);

    // Send the CSRF token to prevent the 403 forbidden error.
    xhr.setRequestHeader("X-CSRFToken", Cookies.get("csrftoken"));

    // Update the upload progress bar.
    xhr.upload.addEventListener("progress", function (event) {
      const progress = (event.loaded / event.total) * 100;
      attachment.setUploadProgress(progress);
    });

    // Handle when the server responded.
    xhr.addEventListener("load", function (event) {
      if (xhr.status === 200) {
        // Set the image url based on the server response.
        const { url } = JSON.parse(xhr.responseText);
        attachment.setAttributes({ url, href: url });
      } else {
        // Display an error alert to the user when the upload failed.
        Swal.fire({
          title: "Failed to upload attachment!",
          text: "Please try again next time...",
          icon: "error",
        });
      }
    });

    // Perform the request.
    xhr.send(formData);
  }
}
