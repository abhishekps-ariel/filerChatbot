# FILIR System Comprehensive Guide

## Table of Contents
1. [System Overview](#system-overview)
2. [Creating a New Petition - Step-by-Step Process](#creating-a-new-petition---step-by-step-process)
3. [Post-Submission: Adding Judgment Information](#post-submission-adding-judgment-information)
4. [Post-Submission: Adding Foreclosure Sale Information](#post-submission-adding-foreclosure-sale-information)
5. [Petition Status Workflow](#petition-status-workflow)
6. [Frequently Asked Questions](#frequently-asked-questions)

---

## System Overview

The FILIR system is a petition filing and management platform for foreclosure proceedings in Massachusetts. It guides users through a comprehensive 10-step process to create, submit, and manage foreclosure petitions with all required legal documentation and compliance checks.

### Key Features
- **10-Step Petition Creation Process**: Organized workflow from organization selection to final submission
- **Address Autocomplete**: Google Places integration for accurate address entry
- **Digital Signature Support**: Electronic attestation with signature management
- **Post-Submission Updates**: Add Judgment and Foreclosure Sale information after petition submission
- **Real-time Validation**: Field-level validation with helpful error messages
- **Multiple Entity Support**: Handle multiple borrowers and loan assignees
- **Status Tracking**: 8 distinct petition statuses from Draft to Closed

---

## Creating a New Petition - Step-by-Step Process

### Step 1: Organization Selection

**Purpose**: Select the organization filing the petition

**Fields**:
- **Organization** (Required): Search and select from available organizations
  - Features search functionality with 300ms debounce
  - Keyboard navigation support (Arrow Up/Down, Enter, Escape)
  - Dropdown displays organization name and details

**How It Works**:
1. Start typing organization name in the search box
2. System displays matching organizations in dropdown
3. Use arrow keys to navigate or click to select
4. Press Enter to confirm selection or Escape to close dropdown

**API Calls**:
- `getAllOrganizations()` - Loads all organizations on component mount
- `searchOrganizations(query)` - Searches organizations as you type

---

### Step 2: Property Details

**Purpose**: Enter the property address subject to foreclosure

**Required Fields** (marked with *):
- **Street Address Line 1*** - Primary street address
- **City*** - Property city
- **State*** - Property state (must be Massachusetts)
- **ZIP Code*** - 5-digit ZIP code

**Optional Fields**:
- **Street Address Line 2** - Apartment, unit, or additional address info

**Special Features**:
- **Google Places Autocomplete**: 
  - Type address and get suggestions from Google Places API
  - Predictions appear in dropdown below address field
  - Click prediction to auto-fill all address fields
  - Keyboard navigation: Arrow Up/Down to navigate, Enter to select, Escape to close
  
- **Massachusetts-Only Validation**:
  - System validates that property is located in Massachusetts
  - If non-MA address detected, shows error: `addressValidationError`
  - Address verification flag: `isAddressVerified` must be true to proceed
  
- **Auto-Population**:
  - Selecting a Google prediction automatically fills: street1, city, state, zip
  - County information (`propertyCounty`) is also captured

**Common Issues**:
- **"Address not verified"**: Make sure to select from Google predictions or verify manually
- **Out-of-state property**: FILIR only accepts Massachusetts properties

---

### Step 3: Loan Details

**Purpose**: Enter detailed information about the mortgage loan

**Required Fields** (marked with *):
- **Is MIN Applicable?*** - Yes/No radio button
  - If Yes: **MIN Number*** field appears (Mortgage Identification Number)
- **Loan Number*** - The servicer's loan number
- **Petition Loan Type*** - Dropdown selection (e.g., Conventional, FHA, VA, ARM)
- **Lien Position** - First, Second, Third, etc.
- **Loan Term*** - Dropdown showing loan terms from API

**Conditional Fields (ARM Detection)**:
- System auto-detects if loan type includes "ARM" or "ADJUSTABLE"
- Additional fields appear for ARM loans:
  - Interest rate details
  - Adjustment period information
  - Index type
  - Margin details

**Special Features**:
- **Currency Formatting**: 
  - All currency fields use `formatCurrencyInput()` for display
  - Internal storage uses `parseCurrencyInput()` to remove formatting
  - Displays as: $1,234,567.89

- **Loan Type Dropdown**:
  - Populated from `commonData` API
  - Uses `StandardSelect` component
  - Shows loan type descriptions

**Connection to Step 7**:
- Loan characteristics (variable rate, interest-only, negative amortization) affect Form 35B compliance
- If any of these are selected, Step 7 auto-sets "Certain Mortgage Loan" to Yes

**Common Issues**:
- **MIN Number Missing**: Only required if "Is MIN Applicable" is set to Yes
- **Loan Type Not Loading**: Check internet connection, system fetches from API

---

### Step 4: Borrower Details

**Purpose**: Add information for all borrowers on the loan

**Support for Multiple Borrowers**:
- Add unlimited borrowers using "Add Borrower" button
- Remove borrowers with red X button (minimum 1 borrower required)
- Each borrower has identical fields

**Fields Per Borrower**:

**Required** (marked with *):
- **First Name*** - Letters only (auto-sanitized with regex `/[A-Za-z\s]+/g`)
- **Last Name*** - Letters only (auto-sanitized)

**Optional**:
- **Middle Name** - Letters only (auto-sanitized)

**Address Fields**:
- **Street Address 1** - Borrower's street address
- **Street Address 2** - Apt/Unit number
- **City** - Borrower's city
- **State** - Borrower's state
- **ZIP Code** - Borrower's ZIP code

**Special Features**:
- **Primary Borrower Designation**: 
  - Checkbox `borrowerIsPrimary` to mark one borrower as primary
  - Only one borrower can be marked as primary
  
- **Address Autocomplete**:
  - Same Google Places integration as Step 2
  - Predictions dropdown for each borrower
  - Keyboard navigation support
  
- **"Use same as property" Checkbox**:
  - Copies property address from Step 2 to borrower address
  - Checkbox appears: `useSameAsProperty`
  - When checked: auto-fills street1, street2, city, state, zip
  - When unchecked: clears all address fields

**Common Issues**:
- **Name Contains Numbers**: System auto-removes non-letter characters
- **Multiple Borrowers with Same Name**: Allowed, system tracks by array index
- **Forgetting to Set Primary Borrower**: Not enforced but recommended for clarity

---

### Step 5: Filing Entity

**Purpose**: Identify the legal entity filing the petition

**Required Fields** (marked with *):
- **Filing Entity Legal Name*** - Auto-prefilled from organization
- **Filing Entity Role*** - Read-only, populated from user profile
  - Shows filing entity types from API (e.g., Mortgagee, Servicer, Attorney)
  
**Address Fields** (Required):
- **Street Address Line 1***
- **Street Address Line 2** (optional)
- **City***
- **State***
- **ZIP Code***

**Special Features**:
- **Auto-Prefill from Organization**:
  - When organization is selected in Step 1, system automatically populates:
    - `filingEntityLegalName` from organization data
    - Address fields from organization's registered address
  - Shows loading state during organization data fetch

- **Read-Only Role**:
  - Filing entity role comes from user's profile
  - Cannot be changed in petition form
  - Reflects user's organizational relationship

**Data Sources**:
- `organizationService.getOrganizationById()` - Fetches organization details
- User profile API - Provides filing entity types and role

**Common Issues**:
- **Legal Name Not Populating**: Ensure organization selected in Step 1 loaded successfully
- **Can't Change Role**: This is by design - role is tied to your user profile

---

### Step 6: Right to Cure (90-Day Notice)

**Purpose**: Document the 90-day right to cure notice sent to borrowers

**Primary Question**:
- **Was Notice Sent?*** - Yes/No radio button
  - If No: Skip remaining fields in this step
  - If Yes: All fields below become required

**Notice Details** (Required if Notice Sent):
- **Notice Date*** - Date notice was sent to borrower
- **Amount in Default*** - Dollar amount borrower owes (currency formatted)
- **Days Delinquent at Notice*** - Integer, number of days payment was overdue
- **Cure Expiration Date*** - Date by which borrower must cure default (90 days from notice)

**Notice Address Fields** (Required if Notice Sent):
- **Notice Street Address Line 1** - Where notice was sent
- **City**
- **State**
- **ZIP Code**

**Borrower Response Tracking**:
- **Did Borrower Respond Within 30 Days?** - Yes/No
- **Borrower Response Date** - Date of response (if applicable)
- **Proceeded with Right to Cure?** - Yes/No

**Special Features**:
- **Address Autocomplete**:
  - Google Places integration for notice address
  - Prediction dropdown with keyboard navigation
  
- **"Use same as property" Checkbox**:
  - Copies property address from Step 2 to notice address
  - State managed via `useSameAsProperty`
  - Auto-fills all address fields when checked
  
- **Multiple Borrowers Support**:
  - System tracks notice information per borrower
  - If multiple borrowers exist, can set individual notice addresses
  
- **Currency Formatting**:
  - `amountInDefault` displays as formatted currency ($X,XXX.XX)
  - Uses same `formatCurrencyInput`/`parseCurrencyInput` utilities

**Legal Context**:
- Massachusetts law requires 90-day right to cure notice before foreclosure
- Notice must include: amount in default, deadline to cure, consequences of non-cure
- Cure period allows borrower to bring loan current and avoid foreclosure

**Common Issues**:
- **Cure Date Calculation**: System doesn't auto-calculate 90 days - enter manually
- **Multiple Notices**: If notice was re-sent, use most recent notice date
- **Partial Cure**: If borrower paid some but not all, still mark as "did not cure fully"

---

### Step 7: Form 35B Compliance

**Purpose**: Determine if Form 35B compliance certificate is required

**Fields**:
- **Is this a "Certain Mortgage Loan"?*** - Yes/No radio button
  - Auto-set based on loan characteristics from Step 3
  - Read-only if auto-detected as "Certain Mortgage Loan"
  
- **Was Form 35B Provided?*** - Yes/No radio button
  - Only appears if "Certain Mortgage Loan" = Yes
  - Required if applicable

**What is a "Certain Mortgage Loan"?**
A loan is considered a "certain mortgage loan" if it has ANY of these characteristics:
- **Variable Rate** (Adjustable Rate Mortgage/ARM)
- **Interest-Only** payment structure
- **Negative Amortization** allowed

**Auto-Detection Logic**:
```
If Step 3 loan has:
  - variableRate = true, OR
  - interestOnly = true, OR
  - negativeAmortization = true

Then:
  - certainMortgageLoan = true (auto-set, read-only)
  - isCertainMortgageLoanReadOnly = true
```

**Form 35B Requirements**:
- Massachusetts law requires lenders to provide Form 35B for certain mortgage loans
- Form 35B contains disclosures about loan terms and risks
- Must be provided before foreclosure can proceed on these loan types

**Common Issues**:
- **"Why can't I change this field?"**: System auto-detected loan characteristics - it's set correctly
- **"I don't have Form 35B"**: If loan is a certain mortgage loan, Form 35B is legally required - contact lender
- **Not sure if Form 35B was provided**: Check loan closing documents or contact loan servicer

---

### Step 8: Loan Assignees (Previous Loan Assignments)

**Purpose**: Document chain of title if loan has been sold/assigned

**Primary Question**:
- **Are there any previous loan assignees?*** - Yes/No radio button
  - If No: Skip this step entirely
  - If Yes: Add assignee details below

**Support for Multiple Assignees**:
- Add unlimited assignees using "Add Assignee" button
- Remove assignees with red X button (minimum 1 if "Yes" selected)
- Tracks chain of assignments in chronological order

**Fields Per Assignee** (All Required if Assignees Exist):
- **Assignee Name*** - Full legal name of entity
- **Assignee Type*** - Dropdown selection
  - Examples: Bank, Credit Union, Investment Firm, Servicer
  - Populated from `assigneeTypes` API
  - Uses `StandardSelect` component
  
- **Assignee Role*** - Dropdown selection
  - Examples: Previous Holder, Current Servicer, Investor
  - Populated from `assigneeRoles` API
  - Uses `StandardSelect` component

**Address Fields** (Required for each assignee):
- **Street Address Line 1***
- **Street Address Line 2** (optional)
- **City***
- **State***
- **ZIP Code***

**Special Features**:
- **Address Autocomplete**:
  - Google Places integration for each assignee
  - Separate prediction dropdown per assignee
  - Keyboard navigation: Arrow Up/Down, Enter, Escape
  - Loading state per assignee: `isLoadingLoanAssigneePredictions[index]`
  
- **"Use same address as Property" Checkbox**:
  - Available for each assignee individually
  - Managed via `useSameAsProperty[index]` state
  - When checked: copies property address from Step 2
  - When unchecked: clears address fields for that assignee
  
- **Address Validation**:
  - Each assignee has separate validation: `loanAssigneeAddressValidationErrors`
  - Error messages display per field per assignee

**Why This Matters**:
- Chain of title must be documented for legal foreclosure proceedings
- Court requires proof that current holder has legal right to foreclose
- Missing assignee information can delay or invalidate foreclosure action

**Common Issues**:
- **Don't know assignment history**: Contact loan servicer for MERS or assignment records
- **Too many assignees**: Document all known assignments - no limit in system
- **Assignee Type vs Role confusion**: 
  - Type = What kind of entity (Bank, Servicer, etc.)
  - Role = Their relationship to loan (Previous Holder, Current Owner, etc.)

---

### Step 9: Petition Attestation (Digital Signature)

**Purpose**: Electronically sign and certify the petition

**Attester Details** (Auto-Filled from User Profile):
All fields are **read-only** and prefilled from your user profile:

- **First Name*** - Signer's first name
- **Middle Initial** - Signer's middle initial (optional)
- **Last Name*** - Signer's last name
- **Email Address*** - Signer's email
- **Title*** - Signer's job title/position

**Digital Signature Requirement**:

**If Signature Available**:
- Green success badge: "Available"
- Signature preview displayed (max 400px width, 120px height)
- Can proceed to certification checkbox

**If Signature Missing**:
- Red danger badge: "Required"
- Warning message: "Digital signature is required to submit this petition"
- "Go to Profile to Upload" button
  - Clicking closes petition modal
  - Navigates to Profile page (`ROUTES.PROFILE`)
  - Upload signature in profile settings
  
**Certification Checkbox**:
- **Electronic Certification*** - Required to proceed
  - Full text: "I certify under penalty of perjury that the information provided in this petition is true and correct to the best of my knowledge"
  - Disabled if no signature uploaded
  - Must be checked to enable "Submit" button

**Submission Timestamp**:
- Automatically captured when petition is submitted
- Displayed as: "Submission timestamp will be captured upon final submission"
- Provides legal record of submission time

**Special Features**:
- **Focus Trap**: Modal captures keyboard focus for accessibility
- **Signature Display Formats**:
  - Supports `signatureUrl` from server
  - Supports `signatureBase64` for inline data
  - Image formats: PNG, JPEG, SVG
  
**Legal Significance**:
- Electronic signature has same legal weight as handwritten signature
- Attestation confirms accuracy of petition under penalty of perjury
- Timestamp provides legal proof of when petition was filed

**Common Issues**:
- **"Can't check certification box"**: Upload digital signature in Profile first
- **"Signature not showing"**: Refresh page or re-upload signature in Profile
- **"Wrong person's name"**: Contact administrator - user profile needs update
- **Changing signature**: Go to Profile > Upload new signature > Return to petition

---

### Step 10: Review and Submit

**Purpose**: Final review of all petition details before submission

**Layout**:
Step 10 displays a comprehensive read-only summary organized by sections. Each section has an "Edit" button to jump back to the corresponding step.

**Summary Sections**:

1. **Property Information** (from Step 2)
   - Street Address (lines 1 & 2)
   - City, State, ZIP Code
   - County
   - Edit button → Returns to Step 2

2. **Loan Information** (from Step 3)
   - Loan Number
   - MIN Number (if applicable)
   - Loan Type (name from dropdown selection)
   - Lien Position
   - Loan Term (description from API)
   - Edit button → Returns to Step 3

3. **Borrower Details** (from Step 4)
   - Lists all borrowers with:
     - Full Name (First Middle Last)
     - Primary Borrower indicator
     - Complete address
   - Edit button → Returns to Step 4

4. **Filing Entity** (from Step 5)
   - Legal Name
   - Role (filing entity type)
   - Complete address
   - Edit button → Returns to Step 5

5. **Right to Cure Notice** (from Step 6)
   - Notice Sent status
   - If sent:
     - Notice Date
     - Amount in Default (formatted currency)
     - Days Delinquent
     - Cure Expiration Date
     - Notice Address
     - Borrower Response details
   - Edit button → Returns to Step 6

6. **Form 35B Compliance** (from Step 7)
   - Certain Mortgage Loan status
   - Form 35B Provided status
   - Edit button → Returns to Step 7

7. **Loan Assignees** (from Step 8)
   - Previous Assignees status
   - If exist:
     - Each assignee with name, type, role, address
   - Edit button → Returns to Step 8

8. **Attestation** (from Step 9)
   - Attester Name
   - Email and Title
   - Digital Signature Preview
   - Certification Status
   - Edit button → Returns to Step 9

**Special Features**:

- **Visual Organization**:
  - Each section has styled header with theme color
  - Clean card-based layout
  - Consistent spacing and typography
  
- **Edit Functionality**:
  - `handleEditSection(stepNumber)` - Jumps to specific step
  - Preserves all entered data
  - Returns to Step 10 when done editing
  
- **Dropdown Value Resolution**:
  - System looks up dropdown values and displays names/descriptions
  - Example: `petitionLoanTypeId` displays as full loan type name
  - Uses helper functions:
    - `getLoanTypes()` - Resolves loan type IDs
    - `getLienPositions()` - Resolves lien position values
    - `getLoanTerms()` - Resolves loan term IDs
    - `getAssigneeTypes()` - Resolves assignee type IDs
    - `getAssigneeRoles()` - Resolves assignee role IDs

**Submission Process**:
1. Review all sections carefully
2. Click "Edit" on any section that needs changes
3. Return to Step 10 when all edits complete
4. Click "Submit Petition" button at bottom
5. System validates all required fields
6. If valid: Petition submitted and status changes to "Submitted"
7. If invalid: Error messages display, jumps to first error

**Common Issues**:
- **Can't submit**: Check for validation errors - system will highlight problem areas
- **Missing information**: Use Edit buttons to add missing required fields
- **Dropdown shows ID instead of name**: Temporary display issue - refresh page
- **Want to change signature**: Must go to Profile, can't edit from Step 10 summary

---

## Post-Submission: Adding Judgment Information

**When to Use**:
After petition status changes to "Submitted" or later, you can add Judgment information to document court decisions.

**Access**:
- Navigate to petition details page
- Click "Edit Judgment" button in Judgment section
- Opens `EditJudgementModal`

**Judgment Fields**:

**Required Fields** (marked with *):
- **Judgment Date*** - Date court issued judgment
  - Date picker format: YYYY-MM-DD
  - Uses `formatDateForInput()` utility for display
  
- **Judgment Type*** - Dropdown selection
  - Options from `judgmentTypes` API enum:
    - Examples: Default Judgment, Summary Judgment, Consent Judgment
  - Uses `StandardSelect` component
  - Stores as integer value
  
- **Court Information*** - Text field
  - Court name and location
  - Example: "Suffolk Superior Court, Boston, MA"
  - Accepts alphanumeric characters
  
- **Docket Numbers*** - Text field
  - Court case/docket numbers
  - Example: "2024-CV-00123"
  - Accepts alphanumeric and special characters (hyphens, slashes)
  - Can include multiple docket numbers separated by commas

**Special Features**:

- **Auto-Fill from Existing Data**:
  - If judgment already exists in petition details, modal pre-populates fields
  - Preserves existing judgment ID for updates
  
- **Field Validation**:
  - Real-time validation with `fieldErrors` state
  - Error messages display below each invalid field
  - Date validation ensures proper format
  
- **Save Behavior**:
  - Calls `onSave(formData)` when "Save" button clicked
  - Updates `formData.judgment` object:
    ```javascript
    {
      id: "existing-judgment-id", // if updating
      judgmentDate: "2024-01-15",
      judgmentType: 1, // integer enum value
      courtInformation: "Suffolk Superior Court",
      docketNumbers: "2024-CV-00123"
    }
    ```
  
- **Loading State**:
  - `isSaving` flag prevents duplicate submissions
  - Button shows spinner during save operation
  - Success toast message on successful save

**Why Judgment Information Matters**:
- Court judgment legally authorizes foreclosure to proceed
- Required before scheduling foreclosure sale
- Provides legal record for property title transfer
- Judgment type affects timeline and procedures

**Common Issues**:
- **Can't add judgment before submission**: Must submit petition first
- **Invalid date format**: Use date picker or format as YYYY-MM-DD
- **Docket number with spaces**: Spaces are preserved - format as court requires
- **Multiple judgments**: System stores one judgment per petition - use most recent

---

## Post-Submission: Adding Foreclosure Sale Information

**When to Use**:
After judgment is added and foreclosure sale has occurred or is scheduled, add sale details.

**Access**:
- Navigate to petition details page
- Click "Edit Foreclosure Sale" button in Foreclosure Sale section
- Opens `EditForeclosureModal`

**Foreclosure Sale Fields**:

**Basic Sale Information** (Required):
- **Sale Date*** - Date foreclosure sale occurred/scheduled
- **Sold To*** - Dropdown selection from `buyerTypes` API:
  - Mortgagee/Investor - Original lender or investor
  - Third Party Buyer - Unrelated purchaser
  - Other
- **Sale Amount*** - Final sale price
  - Currency formatted: $XXX,XXX.XX
  - Uses `formatCurrencyInput()` and `parseCurrencyInput()` utilities
  - Stored as decimal number in database

**Conditional Fields (If Sold to Mortgagee/Investor)**:

When `soldToId` is "Mortgagee" or "Investor", additional fields appear:

- **Vesting Entity Name** - Legal name for property vesting
- **REO Entity Name*** - Real Estate Owned entity name (required)
- **REO Contact First Name*** - First name of REO contact
- **REO Contact Last Name*** - Last name of REO contact
- **REO Business Phone*** - Business phone number
- **REO Emergency Phone*** - 24/7 emergency contact number

**Foreclosure Alternative Questions**:

- **Did Borrower Request Alternative to Foreclosure?** - Yes/No
  - If Yes: **Foreclosure Alternative Option*** becomes required
  - Dropdown options from API:
    - Short Sale
    - Deed in Lieu
    - Loan Modification
    - Repayment Plan
    - Other

**Special Features**:

- **Buyer Type Detection**:
  - System uses `isMortgageeOrInvestor()` helper function
  - Checks if buyer type name/value includes "mortgagee" or "investor"
  - Auto-shows/hides REO fields based on selection
  
- **Phone Number Formatting**:
  - Accepts various formats: (123) 456-7890, 123-456-7890, 1234567890
  - No strict formatting enforced - enter as preferred
  
- **Currency Validation**:
  - `saleAmount` must be positive number
  - Displays with thousands separators and 2 decimal places
  - Example: $250,000.00
  
- **Conditional Validation**:
  - REO fields only validated if `soldToId` is Mortgagee/Investor
  - Foreclosure alternative option only required if requested = Yes
  
- **Form Persistence**:
  - Updates `formData.foreclosureSale` object
  - Preserves existing foreclosure sale ID for updates
  - All fields optional on initial save, can complete in stages

**Sale Process Context**:
1. Judgment obtained (Step: Add Judgment)
2. Notice of Sale published (21 days before sale)
3. Foreclosure auction conducted
4. Property sold to highest bidder or reverts to mortgagee
5. Sale details recorded in system (this step)
6. Deed prepared and recorded

**Common Issues**:
- **REO fields not showing**: Make sure "Sold To" is set to Mortgagee or Investor
- **Sale amount shows $0.00**: Enter amount and include cents (.00)
- **Emergency phone required**: Massachusetts requires 24/7 contact for foreclosed properties
- **Foreclosure alternative after sale**: Mark as "No" if sale already completed
- **Third party buyer with no REO**: REO fields only for Mortgagee/Investor sales

---

## Petition Status Workflow

The FILIR system tracks petitions through 8 distinct statuses:

### Status Definitions and Workflow

1. **Draft (0)** - Initial Status
   - Petition created but not submitted
   - Can edit all fields freely
   - No court review
   - Badge Color: Gray
   - **Actions Available**: Edit, Delete, Submit
   
2. **Submitted (1)** - First Major Milestone
   - Petition submitted to court system
   - Under review by court staff
   - Limited editing (cannot change core petition details)
   - **Can Add**: Judgment information, Foreclosure Sale details
   - Badge Color: Blue
   - **Actions Available**: View, Add Judgment, Add Foreclosure Sale, Add Notes
   
3. **Foreclosure Sale Initiated (2)**
   - Foreclosure sale process has begun
   - Notice of Sale published
   - Sale date scheduled
   - Foreclosure Sale information should be added
   - Badge Color: Orange
   - **Actions Available**: View, Edit Foreclosure Sale, Add Notes
   
4. **Judgment Submitted (3)**
   - Court judgment received and entered
   - Judgment information must be complete
   - Authorizes proceeding with foreclosure
   - Badge Color: Purple
   - **Actions Available**: View, Edit Judgment, Proceed to Sale
   
5. **Returned (4)** - Requires Action
   - Court returned petition with issues
   - Deficiencies must be corrected
   - Check notes for specific issues
   - Can resubmit after corrections
   - Badge Color: Red
   - **Actions Available**: Edit (limited), View Notes, Resubmit
   
6. **Resubmitted (5)** - After Corrections
   - Petition corrected and resubmitted
   - Under review again
   - Awaiting court decision
   - Badge Color: Yellow
   - **Actions Available**: View, Add Notes
   
7. **Accepted (6)** - Approved
   - Court accepted petition
   - All requirements met
   - Can proceed with foreclosure process
   - Badge Color: Green
   - **Actions Available**: View, Proceed with Foreclosure, Add Foreclosure Sale
   
8. **Closed (7)** - Final Status
   - Foreclosure process complete
   - Property sold or otherwise resolved
   - No further actions needed
   - Archive status
   - Badge Color: Dark Gray
   - **Actions Available**: View Only (read-only)

### Status Transitions

**Normal Flow**:
```
Draft → Submitted → Judgment Submitted → Accepted → Foreclosure Sale Initiated → Closed
```

**If Issues Found**:
```
Submitted → Returned → [Fix Issues] → Resubmitted → Accepted
```

**Alternative Paths**:
- **Draft → Deleted**: User can delete draft petitions
- **Any Status → Notes Added**: Notes can be added at any stage
- **Submitted/Accepted → Foreclosure Sale Initiated**: Can add sale details when sale scheduled

### Status-Based Permissions

**Can Edit Core Petition Details**:
- Draft ✅
- All Other Statuses ❌

**Can Add Judgment**:
- Submitted ✅
- Judgment Submitted ✅ (edit existing)
- Foreclosure Sale Initiated ✅
- Accepted ✅

**Can Add Foreclosure Sale**:
- Judgment Submitted ✅
- Foreclosure Sale Initiated ✅
- Accepted ✅
- Closed ✅ (view only)

**Can Add Notes**:
- All Statuses ✅

### Checking Petition Status

**In Petition List**:
- Status badge displayed next to petition number
- Color-coded for quick identification
- Sortable by status

**In Petition Details**:
- Status displayed prominently at top
- Status history/timeline (if available)
- Current actions available based on status

**Status Queries**:
- Use `getSortColumn()` utility to map status to API sort parameter
- Filter petitions by status in petition list view
- Status enum values used in API requests (0-7)

---

## Frequently Asked Questions

### General Questions

**Q: What is FILIR?**
A: FILIR is a foreclosure petition filing system for Massachusetts. It streamlines the petition process, ensures compliance with state requirements, and tracks petitions from creation through foreclosure sale completion.

**Q: Who can use FILIR?**
A: FILIR is used by mortgagees, loan servicers, foreclosure attorneys, and authorized representatives filing foreclosure petitions in Massachusetts courts.

**Q: Is FILIR available for other states?**
A: No, FILIR is specifically designed for Massachusetts foreclosure laws and procedures. All properties must be located in Massachusetts.

---

### Account and Access

**Q: How do I get access to FILIR?**
A: Contact your organization's FILIR administrator. They will create a user account and assign appropriate permissions based on your role.

**Q: I forgot my password. How do I reset it?**
A: Use the "Forgot Password" link on the login page. Enter your email address and follow the reset instructions sent to your email.

**Q: Can I have multiple organizations on one account?**
A: Yes, users can be associated with multiple organizations. Select the appropriate organization in Step 1 of the petition process.

**Q: How do I upload my digital signature?**
A: Navigate to Profile page → Digital Signature section → Upload signature image (PNG or JPEG) → Save. Signature must be uploaded before submitting petitions.

---

### Petition Creation

**Q: Can I save a petition and come back later?**
A: Yes! Petitions are automatically saved as "Draft" status. You can close the form and return later to complete it. Access drafts from the petition list.

**Q: How long do I have to complete a draft petition?**
A: Draft petitions can remain in the system indefinitely. However, it's recommended to complete and submit within 30 days to ensure information remains current.

**Q: Can I delete a petition?**
A: You can only delete petitions with "Draft" status. Once submitted, petitions cannot be deleted but can be closed/withdrawn through proper channels.

**Q: What if I make a mistake after submitting?**
A: After submission, you cannot edit core petition details. If the court finds issues, they'll return the petition with status "Returned." You can then make corrections and resubmit.

**Q: Do I need to complete all 10 steps in one session?**
A: No, your progress is saved automatically. You can complete steps over multiple sessions. The system remembers which step you're on.

---

### Property and Address Questions

**Q: Why is my address not being accepted?**
A: FILIR only accepts Massachusetts addresses. Ensure:
1. Property is actually in Massachusetts
2. You selected from Google autocomplete predictions
3. Address is verified (green checkmark appears)

**Q: The Google autocomplete isn't showing my address.**
A: Try these steps:
1. Type the full street address
2. Include city and state in search
3. If rural address, try entering just street name and number
4. Manual entry available if autocomplete fails - ensure address is verified

**Q: Can I enter a PO Box as property address?**
A: No, the property address must be the physical location of the real estate being foreclosed. PO Boxes are not accepted.

**Q: What if the property has multiple addresses (corner lot, dual entrances)?**
A: Use the primary/official address as recorded in the property's mortgage documents and county registry.

---

### Loan Information Questions

**Q: What is a MIN number?**
A: MIN (Mortgage Identification Number) is a unique 18-digit number assigned by MERS (Mortgage Electronic Registration Systems). Not all loans have a MIN - only select "Yes" if your loan is registered with MERS.

**Q: How do I find the loan number?**
A: The loan number is typically found on:
- Mortgage statements
- Loan servicer correspondence
- Original loan documents
- Servicer's online portal

**Q: What if the loan has been sold multiple times?**
A: Use the **current** loan servicer's loan number in Step 3. Document the assignment history in Step 8 (Loan Assignees).

**Q: What's the difference between loan type and lien position?**
A: 
- **Loan Type**: The kind of loan (Conventional, FHA, VA, ARM, etc.)
- **Lien Position**: Priority of the mortgage (First = primary mortgage, Second = home equity line, etc.)

**Q: What is Form 35B?**
A: Form 35B is a Massachusetts-required disclosure form for "certain mortgage loans" (variable rate, interest-only, or negative amortization). Lenders must provide this to borrowers before closing.

---

### Borrower Information Questions

**Q: What if I have more than 4 borrowers?**
A: No problem! Click "Add Borrower" for each additional borrower. FILIR supports unlimited borrowers on a single petition.

**Q: The borrower's middle name is unknown.**
A: Middle name is optional. Leave blank if unknown.

**Q: Can borrowers have the same name?**
A: Yes, the system can handle multiple borrowers with identical names (e.g., Sr./Jr., common names). Each is tracked separately in the borrowers array.

**Q: What if a borrower's address is different from the property address?**
A: That's common, especially if borrowers moved after defaulting. Enter the borrower's current address where they can receive legal notices.

**Q: Should I mark a primary borrower?**
A: While not strictly required, it's best practice to designate the primary borrower (usually the first name on the mortgage documents).

---

### Right to Cure (Step 6) Questions

**Q: What is the 90-day right to cure?**
A: Massachusetts law requires lenders to give borrowers 90 days to "cure" (fix) their default by paying what's owed before foreclosure can proceed.

**Q: We sent multiple right to cure notices. Which date do I use?**
A: Use the **most recent** valid right to cure notice date. This is the one that starts the 90-day clock.

**Q: What should I enter for "Amount in Default"?**
A: The total amount the borrower must pay to cure, including:
- Missed monthly payments
- Late fees
- Escrow shortages
- Other charges permitted by the mortgage

**Q: How do I calculate the cure expiration date?**
A: Add 90 days to the notice date. Example: Notice sent January 1st, cure expires April 1st. Note: Some mortgage documents may specify a different cure period - consult legal counsel if unsure.

**Q: The borrower made a partial payment. Did they cure?**
A: No. Unless the full amount in default was paid by the cure expiration date, the default was not cured. Mark "No" for proceeded with right to cure.

**Q: Do I need to track if the borrower responded?**
A: These fields are helpful for record-keeping but not required. If borrower contacted you requesting assistance or disputing the default, document it here.

---

### Loan Assignees (Step 8) Questions

**Q: What are loan assignees?**
A: Assignees are entities to whom the loan has been sold or transferred. If the current loan holder is not the original lender, there have been assignments.

**Q: How do I find the assignment history?**
A: Check:
- MERS (Mortgage Electronic Registration System) records
- County registry of deeds
- Loan servicer transfer notices
- Contact your servicing department

**Q: What if I don't know the complete assignment chain?**
A: Document all **known** assignments. Work with your legal team to research any gaps, as incomplete chain of title can delay foreclosure.

**Q: What's the difference between Assignee Type and Assignee Role?**
A: 
- **Type**: What kind of entity (Bank, Credit Union, Investment Company, Servicer)
- **Role**: Their relationship to the loan (Previous Holder, Current Owner, Servicer)

Example: "Wells Fargo" might be Type: Bank, Role: Previous Holder

**Q: Should the current servicer be listed as an assignee?**
A: Only if the **loan ownership** was transferred to them. If they're just servicing the loan on behalf of an investor, they're not an assignee - just a servicer.

---

### Digital Signature and Attestation Questions

**Q: My signature isn't uploading. What formats are accepted?**
A: FILIR accepts:
- PNG (preferred, transparent background)
- JPEG/JPG
- File size: Under 2MB
- Dimensions: Recommended 400x120 pixels or similar aspect ratio

**Q: Can I use a typed/electronic signature?**
A: Yes, as long as it's uploaded in your profile. You can:
- Sign on paper and scan
- Use a digital signature pad
- Use signature software to create electronic signature
- Type your name in cursive font and save as image

**Q: Can someone else sign on my behalf?**
A: No. The digital signature must belong to the person whose name is in the user profile. If signing authority has changed, update your profile or create new user account.

**Q: I updated my signature but it's not showing in the petition.**
A: Try these steps:
1. Save the petition (if in progress)
2. Close the petition modal
3. Refresh the page
4. Reopen the petition
5. Navigate to Step 9 - new signature should appear

**Q: What does "certify under penalty of perjury" mean?**
A: It means you're swearing that all information in the petition is true and accurate to the best of your knowledge. Providing false information can result in legal penalties.

---

### Post-Submission: Judgment and Foreclosure Sale

**Q: When should I add judgment information?**
A: Add judgment information as soon as the court issues a judgment in your foreclosure case. This is typically several weeks to months after petition submission.

**Q: Can I add foreclosure sale details before judgment?**
A: Technically yes in the system, but legally you should have a judgment before scheduling a foreclosure sale. Follow proper legal sequence.

**Q: What if the foreclosure sale was postponed?**
A: Update the sale date in the Edit Foreclosure Sale modal to reflect the new sale date. You can update this information as many times as needed.

**Q: The property sold to a third party. Do I still need REO information?**
A: No, REO (Real Estate Owned) fields are only required if the property reverted to the mortgagee/investor. For third-party sales, those fields are optional.

**Q: What is a "foreclosure alternative"?**
A: These are alternatives to completing the foreclosure sale, such as:
- **Short Sale**: Property sold for less than owed, with lender approval
- **Deed in Lieu**: Borrower voluntarily deeds property to lender
- **Loan Modification**: Loan terms modified to make payments affordable
- **Repayment Plan**: Borrower catches up on missed payments over time

**Q: How do I record a short sale or deed in lieu?**
A: 
1. Add Foreclosure Sale information
2. Set "Requested Alternative to Foreclosure" = Yes
3. Select the specific alternative (Short Sale or Deed in Lieu)
4. Complete sale details as applicable
5. Mark petition status as Closed when finalized

---

### Status and Workflow Questions

**Q: What does "Returned" status mean?**
A: The court reviewed your petition and found deficiencies that must be corrected. Check the Notes section for specific issues. Correct the problems and resubmit.

**Q: How long does it take for a petition to be reviewed?**
A: Review times vary by court workload. Typically:
- Initial review: 5-10 business days
- After corrections: 3-5 business days
- Check with your local court for specific timelines

**Q: Can I withdraw a submitted petition?**
A: You cannot withdraw directly in FILIR. Contact the court clerk or your legal team to initiate withdrawal proceedings. Petition can then be marked as Closed.

**Q: What's the difference between "Accepted" and "Judgment Submitted"?**
A: 
- **Accepted**: Court accepted your petition as properly filed
- **Judgment Submitted**: Court issued a judgment authorizing foreclosure

These can occur in either order depending on court procedures.

**Q: Why can't I edit my petition after submission?**
A: Once submitted, petitions become official court documents. Changes require court approval. If corrections are needed, the court will return the petition with "Returned" status, allowing limited edits.

---

### Technical Issues

**Q: The system is running slow or not loading.**
A: Try these steps:
1. Refresh the page (F5)
2. Clear browser cache
3. Try a different browser (Chrome, Firefox, Edge)
4. Check internet connection
5. Contact IT support if problem persists

**Q: I'm getting an error when trying to save.**
A: Common causes:
- Required fields not completed (check for red asterisks)
- Invalid data format (dates, currency amounts)
- Session timeout (save and log back in)
- Network interruption (check connection)

**Q: Dropdowns are not loading options.**
A: This usually indicates:
- Temporary API connectivity issue - wait 30 seconds and try again
- System maintenance - check for announcements
- Browser compatibility issue - update to latest browser version

**Q: Can I use FILIR on mobile/tablet?**
A: FILIR is optimized for desktop use. While it may function on tablets, the complex multi-step form is best completed on a desktop or laptop for optimal user experience.

**Q: My autocomplete predictions aren't appearing.**
A: This is a Google Places API issue. Try:
- Wait a few seconds after typing
- Type more of the address
- Check internet connection
- Try manual address entry

---

### Best Practices

**Q: What are the most common mistakes when creating petitions?**
A:
1. **Not selecting address from autocomplete** - Always choose from predictions
2. **Missing right to cure documentation** - Ensure all notice details are complete
3. **Incomplete loan assignee chain** - Research full assignment history
4. **Forgetting to upload signature** - Do this BEFORE starting petition
5. **Wrong loan number** - Use current servicer's number, not original lender's

**Q: How can I speed up the petition creation process?**
A: Tips for efficiency:
1. Gather all documents before starting (loan docs, notices, assignments)
2. Upload digital signature in Profile beforehand
3. Have borrower information organized (names, addresses)
4. Know your loan details (MIN, loan type, terms)
5. Save drafts and complete in stages if needed

**Q: Should I add notes to petitions?**
A: Yes! Notes are valuable for:
- Documenting phone calls with borrowers
- Recording unusual circumstances
- Tracking court communications
- Team collaboration
- Future reference

**Q: How often should I check petition status?**
A: 
- After submission: Check every 2-3 business days
- After "Returned" status: Daily until issues resolved
- After "Accepted": Weekly until sale scheduled
- Set up email notifications if available

---

### Getting Help

**Q: I have a question not answered here. Where can I get help?**
A: Contact support through:
1. Your organization's FILIR administrator
2. FILIR Help Desk (if available)
3. User training resources
4. Legal team for legal/procedural questions

**Q: Is there training available for FILIR?**
A: Yes, contact your organization administrator about:
- Initial user training sessions
- Video tutorials
- User documentation
- One-on-one training for specific needs

**Q: Can I suggest improvements to FILIR?**
A: Absolutely! User feedback is valuable. Submit suggestions through:
- Feedback form in FILIR
- Your organization's FILIR administrator
- Regular user feedback sessions

---

## Additional Resources

### Important Legal Disclaimers

**FILIR is a petition management tool, not legal advice.**
- Consult qualified foreclosure attorney for legal questions
- FILIR does not verify legal accuracy of information entered
- Users responsible for ensuring compliance with all applicable laws
- Massachusetts foreclosure laws subject to change

### Massachusetts Foreclosure Law References

- **M.G.L. c. 244, § 14**: Power of sale foreclosures
- **M.G.L. c. 244, § 15**: Notice requirements
- **M.G.L. c. 244, § 35A-35C**: Form 35B requirements
- **90-Day Right to Cure**: M.G.L. c. 244, § 35A

### Key Timeframes (Massachusetts)

- **Right to Cure Period**: 90 days from notice
- **Notice of Sale**: 21 days before sale
- **Redemption Period**: None (Massachusetts has no post-sale redemption)
- **Confirmation of Sale**: Varies by court

### System Terminology

- **MIN**: Mortgage Identification Number (MERS)
- **REO**: Real Estate Owned (lender-owned after foreclosure)
- **Lien Position**: Priority order of mortgages (1st, 2nd, etc.)
- **Form 35B**: Certain mortgage loan disclosure
- **Assignee**: Entity loan was sold/transferred to
- **Attestation**: Legal certification under oath

---

*This guide was last updated: January 2024*

*For technical support or questions, contact your FILIR administrator*
