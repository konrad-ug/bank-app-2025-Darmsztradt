// Page Object for MFI UG employee search
class MfiPage {
    constructor(page) {
        this.page = page;
        this.mainUrl = 'https://mfi.ug.edu.pl/';
    }

    async goto() {
        await this.page.goto(this.mainUrl);
        await this.page.waitForLoadState('networkidle');
    }

    async clickWorkers() {
        await this.page.click('a:has-text("Pracownicy")');
        await this.page.waitForLoadState('networkidle');
    }

    async clickStaffList() {
        await this.page.click('a:has-text("skład osobowy")');
        await this.page.waitForLoadState('networkidle');
    }

    async searchEmployee(name) {
        const searchInput = this.page.locator('input[type="text"], input[type="search"]').first();
        await searchInput.fill(name);
        await this.page.keyboard.press('Enter');
        await this.page.waitForTimeout(2000);
    }

    async clickEmployeeByName(name) {
        await this.page.click(`a:has-text("${name}")`);
        await this.page.waitForLoadState('networkidle');
    }

    getEmployeeLink(name) {
        return this.page.locator(`a:has-text("${name}")`);
    }
}

module.exports = { MfiPage };
