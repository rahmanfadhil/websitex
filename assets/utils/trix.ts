import * as Cookies from "js-cookie";
import reverse from "./reverse";

async function showErrorMessage() {
  const { default: Swal } = await import("sweetalert2");
  await Swal.fire({
    title: "Failed to upload attachment!",
    text: "Please try again next time...",
    icon: "error",
  });
}

/**
 * Handle attachment upload
 *
 * @see https://github.com/basecamp/trix#storing-attached-files
 * @see https://trix-editor.org/js/attachments.js
 */
export async function trixAttachmentAdd({ attachment }: any) {
  if (attachment.file) {
    try {
      // Store the image to a form data.
      const formData = new FormData();
      formData.append("file", attachment.file);

      // Initialize
      const xhr = new XMLHttpRequest();
      const url = await reverse("core:js_upload_media");
      xhr.open("POST", url, true);

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
          showErrorMessage();
        }
      });

      // Perform the request.
      xhr.send(formData);
    } catch (err) {
      showErrorMessage();
    }
  }
}
