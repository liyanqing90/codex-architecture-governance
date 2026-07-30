const languageToggle = document.querySelector("[data-language-toggle]");
const menuToggle = document.querySelector("[data-menu-toggle]");
const siteNav = document.querySelector("[data-site-nav]");
const copyStatus = document.querySelector("[data-copy-status]");
let messages = null;
let currentLanguage = "en";
let copyStatusTimer = null;

function readStoredLanguage() {
  try {
    return window.localStorage.getItem("hengmu-language");
  } catch {
    return null;
  }
}

function storeLanguage(language) {
  try {
    window.localStorage.setItem("hengmu-language", language);
  } catch {
    // The language choice remains active for the current page.
  }
}

function preferredLanguage() {
  const stored = readStoredLanguage();
  if (stored === "en" || stored === "zh-CN") return stored;
  return navigator.language.toLowerCase().startsWith("zh") ? "zh-CN" : "en";
}

function setMenu(open) {
  if (!menuToggle || !siteNav) return;
  menuToggle.setAttribute("aria-expanded", String(open));
  const key = open ? "closeMenu" : "openMenu";
  if (messages?.[currentLanguage]?.[key]) {
    menuToggle.setAttribute("aria-label", messages[currentLanguage][key]);
  }
  siteNav.classList.toggle("is-open", open);
  document.body.classList.toggle("menu-open", open);
}

function setLocalizedText(language) {
  const dictionary = messages?.[language];
  if (!dictionary) return;

  document.documentElement.lang = language;
  document.documentElement.dataset.lang = language;
  document.title = dictionary.pageTitle;

  const description = document.querySelector('meta[name="description"]');
  const ogTitle = document.querySelector('meta[property="og:title"]');
  const ogDescription = document.querySelector('meta[property="og:description"]');
  if (description) description.content = dictionary.pageDescription;
  if (ogTitle) ogTitle.content = dictionary.pageTitle;
  if (ogDescription) ogDescription.content = dictionary.pageDescription;

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const value = dictionary[element.dataset.i18n];
    if (value) element.textContent = value;
  });

  document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
    const value = dictionary[element.dataset.i18nAria];
    if (value) element.setAttribute("aria-label", value);
  });

  document.querySelectorAll("[data-i18n-alt]").forEach((element) => {
    const value = dictionary[element.dataset.i18nAlt];
    if (value) element.setAttribute("alt", value);
  });

  document.querySelectorAll("[data-i18n-content]").forEach((element) => {
    const value = dictionary[element.dataset.i18nContent];
    if (value) element.setAttribute("content", value);
  });

  const imageSuffix = language === "zh-CN" ? "Zh" : "En";
  document.querySelectorAll("[data-image-en][data-image-zh]").forEach((element) => {
    element.setAttribute("src", element.dataset[`image${imageSuffix}`]);
  });

  document.querySelectorAll("[data-localized-link]").forEach((element) => {
    element.setAttribute("href", element.dataset[`link${imageSuffix}`]);
  });

  if (languageToggle) {
    languageToggle.textContent = language === "zh-CN" ? "EN" : "中文";
    languageToggle.lang = language === "zh-CN" ? "en" : "zh-CN";
    languageToggle.setAttribute(
      "aria-label",
      language === "zh-CN" ? "Switch to English" : "切换到简体中文",
    );
  }

  currentLanguage = language;
  storeLanguage(language);
  setMenu(false);
}

async function writeClipboard(value) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(value);
    return;
  }

  const textArea = document.createElement("textarea");
  textArea.value = value;
  textArea.setAttribute("readonly", "");
  textArea.style.position = "fixed";
  textArea.style.opacity = "0";
  document.body.appendChild(textArea);
  textArea.select();
  const copied = document.execCommand("copy");
  textArea.remove();
  if (!copied) throw new Error("Clipboard copy was rejected");
}

function showCopyStatus(message) {
  if (!copyStatus) return;
  window.clearTimeout(copyStatusTimer);
  copyStatus.textContent = message;
  copyStatus.classList.add("is-visible");
  copyStatusTimer = window.setTimeout(() => {
    copyStatus.classList.remove("is-visible");
  }, 2800);
}

document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const originalLabel = messages?.[currentLanguage]?.copy ?? "Copy";
    try {
      await writeClipboard(button.dataset.copy);
      button.textContent = messages[currentLanguage].copied;
      button.classList.add("is-copied");
      showCopyStatus(messages[currentLanguage].copiedStatus);
      window.setTimeout(() => {
        button.textContent = originalLabel;
        button.classList.remove("is-copied");
      }, 2800);
    } catch {
      showCopyStatus(messages?.[currentLanguage]?.copyFailed ?? "Copy failed.");
    }
  });
});

languageToggle?.addEventListener("click", () => {
  setLocalizedText(currentLanguage === "en" ? "zh-CN" : "en");
});

menuToggle?.addEventListener("click", () => {
  setMenu(menuToggle.getAttribute("aria-expanded") !== "true");
});

siteNav?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => setMenu(false));
});

window.addEventListener("resize", () => {
  if (window.innerWidth > 820) setMenu(false);
});

async function initializeLocalization() {
  try {
    const response = await fetch("./site/i18n.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`Localization request failed: ${response.status}`);
    messages = await response.json();
    if (languageToggle) languageToggle.disabled = false;
    setLocalizedText(preferredLanguage());
  } catch {
    if (languageToggle) {
      languageToggle.disabled = true;
      languageToggle.title = "Localization unavailable";
    }
  }
}

initializeLocalization();
