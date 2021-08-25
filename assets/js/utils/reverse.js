import Cookies from "js-cookie";

/**
 * Like Django `reverse` function but in JavaScript.
 *
 * @example const url = await reverse("pages:home")
 * @example const url = await reverse("users:user_detail", [1])
 * @example const url = await reverse("users:user_detail", null, { pk: 1 })
 *
 * @param {string} name the view name
 * @param {string[]} args url positional arguments
 * @param {Object} kwargs url keyword arguments
 *
 * @returns {Promise.<string>} Promise object represents the absolute url
 */
export default async function reverse(name, args, kwargs) {
  const response = await fetch("/js-reverse/", {
    method: "POST",
    mode: "same-origin",
    body: JSON.stringify({ name, args, kwargs }),
    headers: {
      "X-CSRFToken": Cookies.get("csrftoken"),
    },
  });
  if (!response.ok) throw new Error("URL pattern invalid!");
  return await response.text();
}
