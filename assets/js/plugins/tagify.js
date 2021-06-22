import Tagify from "@yaireo/tagify";
import "@yaireo/tagify/src/tagify.scss";

/**
 * Initialize the Tagify plugin for multi-tags input.
 *
 * Make sure that the form value is joined with comma separator, so that Django
 * SimpleArrayField can handle it.
 */
export async function initialize() {
  for (const element of document.querySelectorAll("input.tagsinput")) {
    new Tagify(element, {
      originalInputValueFormat: (values) =>
        values.map((item) => item.value).join(","),
    });
  }
}
