let data = null;

/**
 * Get the current page data in JSON format to show notifications from Django
 * messages framework, get the current view name, etc.
 */
export default function getPageData() {
  if (!data) {
    data = JSON.parse(document.getElementById("page_data").textContent);
    return data;
  }
  return data;
}
