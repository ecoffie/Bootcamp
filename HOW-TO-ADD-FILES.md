# How to Add Excel Files to This Project

## Method 1: Drag and Drop (Easiest)

1. **Open Finder** and locate your Excel file
2. **Open Cursor** and make sure the `Bootcamp` folder is visible in the file explorer (left sidebar)
3. **Drag the Excel file** from Finder and **drop it** into the `Bootcamp` folder in Cursor
4. The file will appear in your workspace!

## Method 2: Using Terminal

1. **Open Terminal** in Cursor (or your system terminal)
2. **Navigate to the Bootcamp folder:**
   ```bash
   cd /Users/ericcoffie/Bootcamp
   ```
3. **Copy your Excel file** to this folder:
   ```bash
   cp /path/to/your/file.xlsx .
   ```
   Or if it's on your Desktop:
   ```bash
   cp ~/Desktop/your-file.xlsx .
   ```

## Method 3: Save Directly from Browser

1. **Download the Excel file** from the website (SBA, DoD, etc.)
2. When the download dialog appears, **change the save location** to:
   ```
   /Users/ericcoffie/Bootcamp
   ```
3. Click **Save**

## Method 4: Using File Menu

1. In Cursor, go to **File → Open Folder**
2. Navigate to where your Excel file is located
3. Select the file and click **Open**
4. Or use **File → Add Files to Workspace**

## Recommended Folder Structure

Once you add Excel files, they should go in:
```
Bootcamp/
├── sblo-data-downloads/    ← Put downloaded files here
│   ├── sba-prime-directory.xlsx
│   ├── dod-csp-directory.pdf
│   └── dot-directory.xlsx
└── [other files]
```

## After Adding Files

Once you've added your Excel file(s), run:

```bash
python3 process-manual-files.py
```

This will automatically:
- ✅ Parse all Excel files in `sblo-data-downloads/`
- ✅ Extract SBLO contacts
- ✅ Add them to your compiled list
- ✅ Remove duplicates

## Quick Check

To see if files were added successfully:

```bash
ls -lh sblo-data-downloads/
```

Or check in Cursor's file explorer - you should see your Excel files listed!




