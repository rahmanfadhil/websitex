import "trix";
import "trix/dist/trix.css";
import Swal from "sweetalert2";

/**
 * Initialize the Trix editor.
 */
export function initialize() {
  document.addEventListener("trix-attachment-add", handleTrixAttachment);
}

/**
 * Handle when the user upload an image to the Trix editor.
 */
function handleTrixAttachment({ attachment }) {
  if (attachment.file) {
    // Store the image to a form data.
    const formData = new FormData();
    formData.append("file", attachment.file);

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
