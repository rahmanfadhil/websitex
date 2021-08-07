/**
 * Enable flatpickr plugin for date & time inputs.
 */
export async function initialize() {
  const { default: flatpickr } = await import("flatpickr");

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
