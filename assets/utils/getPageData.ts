interface PageData {
  messages: { message: string; type: string }[];
  view_name: string;
  args: string[];
  kwargs: { [key: string]: string };
}

/**
 * Get the current page data in JSON format to show notifications from Django
 * messages framework, get the current view name, args, kwargs, etc.
 */
export default function getPageData(): PageData {
  const pageDataElement = document.getElementById("page_data");
  if (!pageDataElement || pageDataElement.textContent === null) {
    throw new Error("No page data element found");
  }
  return JSON.parse(pageDataElement.textContent);
}
