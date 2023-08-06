function GetOciTopLevelCommand_analytics() {
    return 'analytics'
}

function GetOciSubcommands_analytics() {
    $ociSubcommands = @{
        'analytics' = 'analytics-instance work-request work-request-error work-request-log'
        'analytics analytics-instance' = 'change-compartment change-network-endpoint create create-private-access-channel create-vanity-url delete delete-private-access-channel delete-vanity-url get get-private-access-channel list scale start stop update update-private-access-channel update-vanity-url'
        'analytics work-request' = 'delete get list'
        'analytics work-request-error' = 'list'
        'analytics work-request-log' = 'list'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_analytics() {
    $ociCommandsToLongParams = @{
        'analytics analytics-instance change-compartment' = 'analytics-instance-id compartment-id from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'analytics analytics-instance change-network-endpoint' = 'analytics-instance-id from-json help if-match max-wait-seconds network-endpoint-details wait-for-state wait-interval-seconds'
        'analytics analytics-instance create' = 'capacity-type capacity-value compartment-id defined-tags description email-notification feature-set freeform-tags from-json help idcs-access-token-file license-type max-wait-seconds name network-endpoint-details wait-for-state wait-interval-seconds'
        'analytics analytics-instance create-private-access-channel' = 'analytics-instance-id display-name from-json help max-wait-seconds private-source-dns-zones subnet-id vcn-id wait-for-state wait-interval-seconds'
        'analytics analytics-instance create-vanity-url' = 'analytics-instance-id ca-certificate-file description from-json help hosts max-wait-seconds passphrase private-key-file public-certificate-file wait-for-state wait-interval-seconds'
        'analytics analytics-instance delete' = 'analytics-instance-id force from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'analytics analytics-instance delete-private-access-channel' = 'analytics-instance-id force from-json help if-match max-wait-seconds private-access-channel-key wait-for-state wait-interval-seconds'
        'analytics analytics-instance delete-vanity-url' = 'analytics-instance-id force from-json help if-match max-wait-seconds vanity-url-key wait-for-state wait-interval-seconds'
        'analytics analytics-instance get' = 'analytics-instance-id from-json help'
        'analytics analytics-instance get-private-access-channel' = 'analytics-instance-id from-json help private-access-channel-key'
        'analytics analytics-instance list' = 'all capacity-type compartment-id feature-set from-json help lifecycle-state limit name page page-size sort-by sort-order'
        'analytics analytics-instance scale' = 'analytics-instance-id capacity from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'analytics analytics-instance start' = 'analytics-instance-id from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'analytics analytics-instance stop' = 'analytics-instance-id from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'analytics analytics-instance update' = 'analytics-instance-id defined-tags description email-notification force freeform-tags from-json help if-match license-type max-wait-seconds wait-for-state wait-interval-seconds'
        'analytics analytics-instance update-private-access-channel' = 'analytics-instance-id display-name force from-json help if-match max-wait-seconds private-access-channel-key private-source-dns-zones subnet-id vcn-id wait-for-state wait-interval-seconds'
        'analytics analytics-instance update-vanity-url' = 'analytics-instance-id ca-certificate-file from-json help if-match max-wait-seconds passphrase private-key-file public-certificate-file vanity-url-key wait-for-state wait-interval-seconds'
        'analytics work-request delete' = 'force from-json help if-match work-request-id'
        'analytics work-request get' = 'from-json help work-request-id'
        'analytics work-request list' = 'all compartment-id from-json help limit page page-size resource-id resource-type sort-by sort-order status'
        'analytics work-request-error list' = 'all from-json help limit page page-size work-request-id'
        'analytics work-request-log list' = 'all from-json help limit page page-size work-request-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_analytics() {
    $ociCommandsToShortParams = @{
        'analytics analytics-instance change-compartment' = '? c h'
        'analytics analytics-instance change-network-endpoint' = '? h'
        'analytics analytics-instance create' = '? c h'
        'analytics analytics-instance create-private-access-channel' = '? h'
        'analytics analytics-instance create-vanity-url' = '? h'
        'analytics analytics-instance delete' = '? h'
        'analytics analytics-instance delete-private-access-channel' = '? h'
        'analytics analytics-instance delete-vanity-url' = '? h'
        'analytics analytics-instance get' = '? h'
        'analytics analytics-instance get-private-access-channel' = '? h'
        'analytics analytics-instance list' = '? c h'
        'analytics analytics-instance scale' = '? h'
        'analytics analytics-instance start' = '? h'
        'analytics analytics-instance stop' = '? h'
        'analytics analytics-instance update' = '? h'
        'analytics analytics-instance update-private-access-channel' = '? h'
        'analytics analytics-instance update-vanity-url' = '? h'
        'analytics work-request delete' = '? h'
        'analytics work-request get' = '? h'
        'analytics work-request list' = '? c h'
        'analytics work-request-error list' = '? h'
        'analytics work-request-log list' = '? h'
    }
    return $ociCommandsToShortParams
}