function GetOciTopLevelCommand_marketplace() {
    return 'marketplace'
}

function GetOciSubcommands_marketplace() {
    $ociSubcommands = @{
        'marketplace' = 'accepted-agreement agreement category listing package publication publication-package publication-summary publisher report-collection report-type-collection tax-summary'
        'marketplace accepted-agreement' = 'create delete get list update'
        'marketplace agreement' = 'get list'
        'marketplace category' = 'list'
        'marketplace listing' = 'get list'
        'marketplace package' = 'get list'
        'marketplace publication' = 'change-compartment create create-publication-create-image-publication-package delete get update'
        'marketplace publication-package' = 'get list'
        'marketplace publication-summary' = 'list-publications'
        'marketplace publisher' = 'list'
        'marketplace report-collection' = 'list-reports'
        'marketplace report-type-collection' = 'list-report-types'
        'marketplace tax-summary' = 'list-taxes'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_marketplace() {
    $ociCommandsToLongParams = @{
        'marketplace accepted-agreement create' = 'agreement-id compartment-id defined-tags display-name freeform-tags from-json help listing-id package-version signature'
        'marketplace accepted-agreement delete' = 'accepted-agreement-id force from-json help if-match signature'
        'marketplace accepted-agreement get' = 'accepted-agreement-id from-json help'
        'marketplace accepted-agreement list' = 'accepted-agreement-id all compartment-id display-name from-json help limit listing-id package-version page page-size sort-by sort-order'
        'marketplace accepted-agreement update' = 'accepted-agreement-id defined-tags display-name force freeform-tags from-json help if-match'
        'marketplace agreement get' = 'agreement-id compartment-id from-json help listing-id package-version'
        'marketplace agreement list' = 'all compartment-id from-json help limit listing-id package-version page page-size'
        'marketplace category list' = 'all compartment-id from-json help limit page page-size'
        'marketplace listing get' = 'compartment-id from-json help listing-id'
        'marketplace listing list' = 'all category compartment-id from-json help is-featured limit listing-id listing-types name operating-systems package-type page page-size pricing publisher-id sort-by sort-order'
        'marketplace package get' = 'compartment-id from-json help listing-id package-version'
        'marketplace package list' = 'all compartment-id from-json help limit listing-id package-type package-version page page-size sort-by sort-order'
        'marketplace publication change-compartment' = 'compartment-id from-json help if-match publication-id'
        'marketplace publication create' = 'compartment-id defined-tags freeform-tags from-json help is-agreement-acknowledged listing-type long-description max-wait-seconds name package-details short-description support-contacts wait-for-state wait-interval-seconds'
        'marketplace publication create-publication-create-image-publication-package' = 'compartment-id defined-tags freeform-tags from-json help is-agreement-acknowledged listing-type long-description max-wait-seconds name package-details-eula package-details-image-id package-details-operating-system package-details-package-version short-description support-contacts wait-for-state wait-interval-seconds'
        'marketplace publication delete' = 'force from-json help if-match max-wait-seconds publication-id wait-for-state wait-interval-seconds'
        'marketplace publication get' = 'from-json help publication-id'
        'marketplace publication update' = 'defined-tags force freeform-tags from-json help if-match long-description max-wait-seconds name publication-id short-description support-contacts wait-for-state wait-interval-seconds'
        'marketplace publication-package get' = 'from-json help package-version publication-id'
        'marketplace publication-package list' = 'all from-json help limit package-type package-version page page-size publication-id sort-by sort-order'
        'marketplace publication-summary list-publications' = 'all compartment-id from-json help limit listing-type name operating-systems page page-size publication-id sort-by sort-order'
        'marketplace publisher list' = 'all compartment-id from-json help limit page page-size publisher-id'
        'marketplace report-collection list-reports' = 'all compartment-id date from-json help page report-type'
        'marketplace report-type-collection list-report-types' = 'all compartment-id from-json help page'
        'marketplace tax-summary list-taxes' = 'all compartment-id from-json help listing-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_marketplace() {
    $ociCommandsToShortParams = @{
        'marketplace accepted-agreement create' = '? c h'
        'marketplace accepted-agreement delete' = '? h'
        'marketplace accepted-agreement get' = '? h'
        'marketplace accepted-agreement list' = '? c h'
        'marketplace accepted-agreement update' = '? h'
        'marketplace agreement get' = '? c h'
        'marketplace agreement list' = '? c h'
        'marketplace category list' = '? c h'
        'marketplace listing get' = '? c h'
        'marketplace listing list' = '? c h'
        'marketplace package get' = '? c h'
        'marketplace package list' = '? c h'
        'marketplace publication change-compartment' = '? c h'
        'marketplace publication create' = '? c h'
        'marketplace publication create-publication-create-image-publication-package' = '? c h'
        'marketplace publication delete' = '? h'
        'marketplace publication get' = '? h'
        'marketplace publication update' = '? h'
        'marketplace publication-package get' = '? h'
        'marketplace publication-package list' = '? h'
        'marketplace publication-summary list-publications' = '? c h'
        'marketplace publisher list' = '? c h'
        'marketplace report-collection list-reports' = '? c h'
        'marketplace report-type-collection list-report-types' = '? c h'
        'marketplace tax-summary list-taxes' = '? c h'
    }
    return $ociCommandsToShortParams
}