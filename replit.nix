{pkgs}: {
  deps = [
    pkgs.chromedriver
    pkgs.chromium
    pkgs.glibcLocales
    pkgs.geckodriver
    pkgs.postgresql
    pkgs.openssl
  ];
}
