// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('MFI UG Employee Tests', () => {

    test('should find Konrad Soltys at Instytut Informatyki', async ({ page }) => {
        await page.goto('https://mfi.ug.edu.pl/');
        await page.waitForLoadState('domcontentloaded');

        await page.click('a:has-text("Pracownicy")');
        await page.waitForLoadState('domcontentloaded');

        await page.goto('https://old.mfi.ug.edu.pl/pracownicy_mfi/sklad_osobowy');
        await page.waitForLoadState('domcontentloaded');

        const konradLink = page.locator('a:has-text("Konrad Sołtys")');
        await expect(konradLink.first()).toBeVisible({ timeout: 30000 });

        await konradLink.first().click();
        await page.waitForLoadState('domcontentloaded');

        await expect(page.locator('body')).toContainText('Nr pokoju: 4.19', { timeout: 30000 });
    });

    test('should find Anna Baran at Instytut Fizyki Doswiadczalnej', async ({ page }) => {
        await page.goto('https://ug.edu.pl/pracownicy/szukaj?letter=B');
        await page.waitForLoadState('domcontentloaded');

        const annaLink = page.locator('a:has-text("Anna Baran")');
        await expect(annaLink.first()).toBeVisible({ timeout: 30000 });

        await annaLink.first().click();
        await page.waitForLoadState('domcontentloaded');

        await expect(page.locator('body')).toContainText('Fizyki Doświadczalnej', { timeout: 30000 });
    });

});
