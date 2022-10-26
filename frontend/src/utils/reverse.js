import Cookies from "js-cookie";

/**
 * Like Django `reverse` function but in JavaScript.
 *
 * @example const url = await reverse("pages:home")
 * @example const url = await reverse("users:user_detail", [1])
 * @example const url = await reverse("users:user_detail", null, { pk: 1 })
 *
 * @see https://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.urls.reverse
 *
 * @param name The name of the URL.
 * @param args The arguments to pass to the URL.
 * @param kwargs The keyword arguments to pass to the URL.
 * @returns {Promise<string>} The URL.
 */
export default async function reverse(name, args, kwargs) {
  const response = await fetch("/js-reverse/", {
    method: "POST",
    mode: "same-origin",
    body: JSON.stringify({ name, args, kwargs }),
    headers: {
      "X-CSRFToken": Cookies.get("csrftoken") || "",
    },
  });
  if (!response.ok) throw new Error("URL pattern invalid!");
  return await response.text();
}
