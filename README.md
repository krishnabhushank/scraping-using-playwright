# Scraping using Playwright

This codebase shows samples of how we can use playwright for scraping

## HowTo Use Playwright on Windows 7

If you Try to install Playwright on Windows 7, you get a message that it it not support on Windows 8.1. Follow the below steps to resolve this issue.

- Download `node-v18.17.0-win-x64.zip` from nodejs.org/en/download
  - ![image2023-7-27 20_25_37.png](images%2Fimage2023-7-27%2020_25_37.png)
- Unzip `node-v18.17.0-win-x64.zip` to `C:\Post\node-v18.17.0-win-x64`
  - ![image2023-7-27 20_28_16.png](images%2Fimage2023-7-27%2020_28_16.png)
- Windows Start > Search for `Envrionment` > Select "Envrionment Variables for your Account", or Go to System-Properties (run: systempropertiesadvanced.exe), in Advanced tab, click Environment Variables
  - ![image2023-7-27 20_32_53.png](images%2Fimage2023-7-27%2020_32_53.png)
- Add NODE_PATH with Value as `C:\Post\node-v18.17.0-win-x64\node_modules`
  - ![image2023-7-27 20_34_31.png](images%2Fimage2023-7-27%2020_34_31.png)
- Add NODE_SKIP_PLATFORM_CHECK With value as 1
  - ![image2023-7-27 20_35_2.png](images%2Fimage2023-7-27%2020_35_2.png)
- In Your Scrapy Session, do `playwright install`