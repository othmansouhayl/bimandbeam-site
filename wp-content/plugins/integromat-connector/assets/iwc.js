(function ($) {
    "use strict";
    $(document).ready(function () {

        // API Key reveal/hide functionality
        let apiKeyTimeout;
        let countdownInterval;
        
        $('#iwc-api-key-toggle').on('click', function() {
            const $button = $(this);
            const $input = $('#iwc-api-key-value');
            const state = $button.data('state');
            
            if (state === 'masked') {
                // Fetch the key dynamically via AJAX
                revealApiKey($button, $input);
            } else {
                // Hide the key
                hideApiKey($button, $input);
            }
        });
        
        // API Key regenerate functionality
        $('#iwc-api-key-regenerate').on('click', function() {
            showRegenerateModal();
        });
        
        function showRegenerateModal() {
            // Create modal HTML
            const modalHtml = `
                <div id="iwc-regenerate-modal" class="iwc-modal">
                    <div class="iwc-modal-content">
                        <div class="iwc-modal-header">
                            <h3>Regenerate API Key</h3>
                            <span class="iwc-modal-close">&times;</span>
                        </div>
                        <div class="iwc-modal-body">
                            <div class="iwc-warning-box">
                                <strong>⚠️ WARNING:</strong> Regenerating the API key will immediately break ALL existing connections between your WordPress site and Make that use this key.
                            </div>
                            
                            <p><strong>This action is irreversible.</strong> You will need to:</p>
                            <ul>
                                <li>Update all your connections with the new API key on Make</li>
                                <li>Test all connections after regeneration</li>
                            </ul>
                            
                            <div class="iwc-checkbox-group">
                                <input type="checkbox" id="iwc-confirm-understand" required>
                                <label for="iwc-confirm-understand">
                                    I understand that this will break all existing connections and this action cannot be undone.
                                </label>
                            </div>
                            
                            <div class="iwc-form-group">
                                <label for="iwc-confirm-text">
                                    Type <strong>"regenerate"</strong> to confirm:
                                </label>
                                <input type="text" id="iwc-confirm-text" placeholder="regenerate" autocomplete="off">
                            </div>
                            
                            <div class="iwc-form-actions">
                                <button type="button" class="button iwc-modal-cancel">Cancel</button>
                                <button type="button" id="iwc-confirm-regenerate" class="button iwc-confirm-btn" disabled>
                                    Regenerate API Key
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Remove existing modal if any
            $('#iwc-regenerate-modal').remove();
            
            // Add modal to body
            $('body').append(modalHtml);
            
            // Show modal
            $('#iwc-regenerate-modal').show();
            
            // Focus on checkbox
            $('#iwc-confirm-understand').focus();
            
            // Enable/disable confirm button based on validation
            function validateForm() {
                const isChecked = $('#iwc-confirm-understand').is(':checked');
                const textMatch = $('#iwc-confirm-text').val().toLowerCase() === 'regenerate';
                $('#iwc-confirm-regenerate').prop('disabled', !(isChecked && textMatch));
            }
            
            $('#iwc-confirm-understand, #iwc-confirm-text').on('change keyup', validateForm);
            
            // Handle confirm button
            $('#iwc-confirm-regenerate').on('click', function() {
                const $button = $(this);
                const originalText = $button.text();
                
                // Show loading state
                $button.text('Regenerating...').prop('disabled', true);
                
                // Make AJAX request
                $.post(iwc_ajax.ajax_url, {
                    action: 'iwc_regenerate_api_key',
                    confirmation: $('#iwc-confirm-text').val(),
                    nonce: iwc_ajax.regenerate_nonce
                })
                .done(function(response) {
                    if (response.success) {
                        // Update the API key field
                        const $input = $('#iwc-api-key-value');
                        const $toggleBtn = $('#iwc-api-key-toggle');
                        
                        // Update data attributes
                        $input.data('masked', response.data.masked_token);
                        
                        // Reset to masked state
                        hideApiKey($toggleBtn, $input);
                        $input.val(response.data.masked_token);
                        
                        // Close modal
                        $('#iwc-regenerate-modal').remove();
                        
                        // Show success message
                        showMessage('API key regenerated successfully! Please update your Make.com connections with the new key.', 'success');
                    } else {
                        showMessage('Error: ' + (response.data || 'Unknown error occurred'), 'error');
                    }
                })
                .fail(function() {
                    showMessage('Failed to regenerate API key. Please try again.', 'error');
                })
                .always(function() {
                    $button.text(originalText).prop('disabled', false);
                });
            });
            
            // Handle modal close
            $('.iwc-modal-close, .iwc-modal-cancel').on('click', function() {
                $('#iwc-regenerate-modal').remove();
            });
            
            // Close modal on outside click
            $('#iwc-regenerate-modal').on('click', function(e) {
                if (e.target === this) {
                    $(this).remove();
                }
            });
        }
        
        // Log purge functionality
        $('#iwc-log-purge').on('click', function() {
            showPurgeModal();
        });
        
        function showPurgeModal() {
            // Create modal HTML
            const modalHtml = `
                <div id="iwc-purge-modal" class="iwc-modal">
                    <div class="iwc-modal-content">
                        <div class="iwc-modal-header">
                            <h3>Purge Log Data</h3>
                            <span class="iwc-modal-close">&times;</span>
                        </div>
                        <div class="iwc-modal-body">
                            <div class="iwc-warning-box">
                                <strong>⚠️ WARNING:</strong> This will permanently delete all stored log data.
                            </div>
                            
                            <p><strong>This action cannot be undone.</strong> All diagnostic and debug information will be lost.</p>
                            
                            <p>Are you sure you want to purge all log data?</p>
                            
                            <div class="iwc-form-actions">
                                <button type="button" class="button iwc-modal-cancel">Cancel</button>
                                <button type="button" id="iwc-confirm-purge" class="button iwc-confirm-btn">
                                    Purge
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Remove existing modal if any
            $('#iwc-purge-modal').remove();
            
            // Add modal to body
            $('body').append(modalHtml);
            
            // Show modal
            $('#iwc-purge-modal').show();
            
            // Handle confirm button
            $('#iwc-confirm-purge').on('click', function() {
                const $button = $(this);
                const originalText = $button.text();
                
                // Show loading state
                $button.text('Purging...').prop('disabled', true);
                
                // Make AJAX request
                $.post(iwc_ajax.ajax_url, {
                    action: 'iwc_purge_logs',
                    nonce: iwc_ajax.purge_nonce
                })
                .done(function(response) {
                    // Close modal
                    $('#iwc-purge-modal').remove();
                    
                    if (response.success) {
                        // Show success message
                        showLogMessage('Log data purged successfully.', 'success');
                        
                        // Disable purge and download buttons since no logs exist
                        $('#iwc-log-purge, .iwc-log-actions a').addClass('disabled').prop('disabled', true);
                    } else {
                        showLogMessage('Error: ' + (response.data || 'Unknown error occurred'), 'error');
                    }
                })
                .fail(function() {
                    $('#iwc-purge-modal').remove();
                    showLogMessage('Failed to purge log data. Please try again.', 'error');
                })
                .always(function() {
                    $button.text(originalText).prop('disabled', false);
                });
            });
            
            // Handle modal close
            $('.iwc-modal-close, .iwc-modal-cancel').on('click', function() {
                $('#iwc-purge-modal').remove();
            });
            
            // Close modal on outside click
            $('#iwc-purge-modal').on('click', function(e) {
                if (e.target === this) {
                    $(this).remove();
                }
            });
        }
        
        function showLogMessage(text, type) {
            // Remove existing messages
            $('.iwc-log-message').remove();
            
            // Create new message
            const $message = $('<div class="iwc-message iwc-log-message ' + type + '">' + text + '</div>');
            
            // Insert after the log actions container
            $('.iwc-log-actions').after($message);
            
            // Auto-remove after 5 seconds for success messages
            if (type === 'success') {
                setTimeout(function() {
                    $message.fadeOut(500, function() {
                        $(this).remove();
                    });
                }, 5000);
            }
        }
        
        function showMessage(text, type) {
            // Remove existing messages
            $('.iwc-message').remove();
            
            // Create new message
            const $message = $('<div class="iwc-message ' + type + '">' + text + '</div>');
            
            // Insert after the API key container
            $('.iwc-api-key-container').after($message);
            
            // Auto-remove after 5 seconds for success messages
            if (type === 'success') {
                setTimeout(function() {
                    $message.fadeOut(500, function() {
                        $(this).remove();
                    });
                }, 5000);
            }
        }
        
        function showTabMessage(text, type, $form) {
            // Remove existing tab messages
            $('.iwc-tab-message').remove();
            
            // Create new message with WordPress native notice styling
            const $message = $('<div class="notice notice-' + type + ' is-dismissible iwc-tab-message"><p>' + text + '</p></div>');
            
            // Insert after the submit button in the current form
            $form.find('.button').after($message);
            
            // Auto-remove after 5 seconds for success messages
            if (type === 'success') {
                setTimeout(function() {
                    $message.fadeOut(500, function() {
                        $(this).remove();
                    });
                }, 5000);
            }
        }
        
        function showSimpleMessage(text, type, $form) {
            // Remove existing simple messages
            $('.iwc-simple-message').remove();
            
            // Create new message with WordPress native notice styling
            const $message = $('<div class="notice notice-' + type + ' is-dismissible iwc-simple-message"><p>' + text + '</p></div>');
            
            // Insert after the submit button in the current form
            $form.find('.button').after($message);
            
            // Auto-remove after 5 seconds for success messages
            if (type === 'success') {
                setTimeout(function() {
                    $message.fadeOut(500, function() {
                        $(this).remove();
                    });
                }, 5000);
            }
        }
        
        function revealApiKey($button, $input) {
            // Show loading state
            const originalText = $button.text();
            $button.text('Loading...').prop('disabled', true);
            
            // Make AJAX request to fetch the API key
            $.post(iwc_ajax.ajax_url, {
                action: 'iwc_reveal_api_key',
                nonce: iwc_ajax.reveal_nonce
            })
            .done(function(response) {
                if (response.success) {
                    const revealedKey = response.data.api_key;
                    
                    // Update input and button state
                    $input.val(revealedKey).attr('data-state', 'revealed');
                    $button.text('Hide').data('state', 'revealed').prop('disabled', false);
                    
                    // Add countdown display
                    const $countdown = $('<span class="iwc-countdown">Auto-hide in 30s</span>');
                    $button.after($countdown);
                    
                    // Countdown timer
                    let secondsLeft = 30;
                    countdownInterval = setInterval(function() {
                        secondsLeft--;
                        $countdown.text(`Auto-hide in ${secondsLeft}s`);
                        
                        if (secondsLeft <= 0) {
                            clearInterval(countdownInterval);
                        }
                    }, 1000);
                    
                    // Auto-hide after 30 seconds
                    apiKeyTimeout = setTimeout(function() {
                        clearInterval(countdownInterval);
                        hideApiKey($button, $input);
                    }, 30000);
                } else {
                    showMessage('Error: ' + (response.data || 'Failed to retrieve API key'), 'error');
                    $button.text(originalText).prop('disabled', false);
                }
            })
            .fail(function() {
                showMessage('Failed to retrieve API key. Please try again.', 'error');
                $button.text(originalText).prop('disabled', false);
            });
        }
        
        function hideApiKey($button, $input) {
            const maskedKey = $input.data('masked');
            $input.val(maskedKey).removeAttr('data-state');
            $button.text('Reveal').data('state', 'masked').removeClass('iwc-hide-btn').addClass('iwc-reveal-btn');
            
            // Remove countdown display
            $button.siblings('.iwc-countdown').remove();
            
            // Clear intervals and timeouts
            if (countdownInterval) {
                clearInterval(countdownInterval);
                countdownInterval = null;
            }
            if (apiKeyTimeout) {
                clearTimeout(apiKeyTimeout);
                apiKeyTimeout = null;
            }
        }

        $('#iwc-api-key-value').on('click', function() {
            $(this).select();
        });

        // Initialize tabs functionality
        initializeTabs();
        
        function initializeTabs() {
            // Native tab functionality
            $('.nav-tab').on('click', function(e) {
                e.preventDefault();
                
                var targetTab = $(this).data('tab');
                
                // Remove active class from all tabs and content
                $('.nav-tab').removeClass('nav-tab-active');
                $('.iwc-tab-content').removeClass('iwc-tab-active');
                
                // Add active class to clicked tab
                $(this).addClass('nav-tab-active');
                
                // Show corresponding content
                $('#iwc-tab-' + targetTab).addClass('iwc-tab-active');
                
                // Store active tab in sessionStorage
                sessionStorage.setItem('iwc-active-tab', targetTab);
                
                // Update ARIA attributes for accessibility
                $('.nav-tab').attr('aria-selected', 'false');
                $(this).attr('aria-selected', 'true');
                
                $('.iwc-tab-content').attr('aria-hidden', 'true');
                $('#iwc-tab-' + targetTab).attr('aria-hidden', 'false');
            });
            
            // Restore active tab from sessionStorage on page load
            var activeTab = sessionStorage.getItem('iwc-active-tab');
            if (activeTab && $('#iwc-tab-' + activeTab).length) {
                $('.nav-tab').removeClass('nav-tab-active');
                $('.iwc-tab-content').removeClass('iwc-tab-active');
                
                $('[data-tab="' + activeTab + '"]').addClass('nav-tab-active');
                $('#iwc-tab-' + activeTab).addClass('iwc-tab-active');
                
                // Update ARIA attributes
                $('.nav-tab').attr('aria-selected', 'false');
                $('[data-tab="' + activeTab + '"]').attr('aria-selected', 'true');
                
                $('.iwc-tab-content').attr('aria-hidden', 'true');
                $('#iwc-tab-' + activeTab).attr('aria-hidden', 'false');
            } else {
                // Ensure first tab is active if no stored tab
                $('.nav-tab:first').addClass('nav-tab-active');
                $('.iwc-tab-content:first').addClass('iwc-tab-active');
                
                // Set ARIA attributes for default state
                $('.nav-tab:first').attr('aria-selected', 'true');
                $('.nav-tab:not(:first)').attr('aria-selected', 'false');
                $('.iwc-tab-content:first').attr('aria-hidden', 'false');
                $('.iwc-tab-content:not(:first)').attr('aria-hidden', 'true');
            }
        }

        // to show waiting animation of the cursor when saving
        $('.iwc-tab-content .button').click(function (e) {
            e.preventDefault();
            
            // Get the form within the active tab
            var $activeTab = $('.iwc-tab-content.iwc-tab-active');
            var $form = $activeTab.find('form');
            
            // Validate form before submission
            var hasErrors = false;
            var $requiredFields = $form.find('[required]');
            
            $requiredFields.each(function() {
                var $field = $(this);
                if (!$field.val() || $field.val().trim() === '') {
                    $field.addClass('error');
                    hasErrors = true;
                } else {
                    $field.removeClass('error');
                }
            });
            
            if (hasErrors) {
                alert('Please fill in all required fields.');
                return false;
            }
            
            $('.imapie_settings_container').addClass('wait');
            
            // Submit the active form
            var formData = $form.serialize();
            
            $.post('options.php', formData)
                .done(function() {
                    $('.imapie_settings_container').removeClass('wait');
                    // Show success message after the submit button
                    showTabMessage('Settings saved successfully.', 'success', $form);
                })
                .fail(function(xhr, status, error) {
                    $('.imapie_settings_container').removeClass('wait');
                    console.error('Form submission failed:', error);
                    // Show error message after the submit button
                    showTabMessage('Error saving settings. Please try again.', 'error', $form);
                });

            return false;
        });

        // Custom Taxonomies form submission handling
        $('#impaie_form_taxonomy .button').click(function (e) {
            e.preventDefault();
            
            // Get the Custom Taxonomies form
            var $form = $('#impaie_form_taxonomy');
            
            // Validate form before submission
            var hasErrors = false;
            var $requiredFields = $form.find('[required]');
            
            $requiredFields.each(function() {
                var $field = $(this);
                if (!$field.val() || $field.val().trim() === '') {
                    $field.addClass('error');
                    hasErrors = true;
                } else {
                    $field.removeClass('error');
                }
            });
            
            if (hasErrors) {
                alert('Please fill in all required fields.');
                return false;
            }
            
            $('.imapie_settings_container').addClass('wait');
            
            // Submit the form
            var formData = $form.serialize();
            
            $.post('options.php', formData)
                .done(function() {
                    $('.imapie_settings_container').removeClass('wait');
                    // Show success message after the submit button
                    showSimpleMessage('Settings saved successfully.', 'success', $form);
                })
                .fail(function(xhr, status, error) {
                    $('.imapie_settings_container').removeClass('wait');
                    console.error('Form submission failed:', error);
                    // Show error message after the submit button
                    showSimpleMessage('Error saving settings. Please try again.', 'error', $form);
                });

            return false;
        });

        $('.uncheck_all').click(function (e) {
            e.preventDefault();
            
            let $button = $(this);
            let uncheckAllStatus = $button.attr('data-status') || '0';
            let isChecking = uncheckAllStatus === '0';

            if (isChecking) {
                $button.attr('data-status', '1');
                $button.text($button.data('uncheck-text') || 'Uncheck All');
            } else {
                $button.attr('data-status', '0');
                $button.text($button.data('check-text') || 'Check All');
            }

            // Target checkboxes in the current active tab only
            var $activeTab = $('.iwc-tab-content.iwc-tab-active');
            if ($activeTab.length) {
                $activeTab.find('input[type="checkbox"]').each(function () {
                    $(this).prop('checked', isChecking);
                });
            } else {
                // Fallback for non-tabbed pages (like General Settings)
                $button.closest('form').find('input[type="checkbox"]').each(function () {
                    $(this).prop('checked', isChecking);
                });
            }
            
            return false;
        });
        
        // Add accessibility improvements
        $('input[type="checkbox"]').on('change', function() {
            $(this).attr('aria-checked', this.checked);
        });
        
        // Add form validation feedback
        $('form input, form select, form textarea').on('blur', function() {
            var $field = $(this);
            if ($field.is('[required]') && (!$field.val() || $field.val().trim() === '')) {
                $field.addClass('error').attr('aria-invalid', 'true');
            } else {
                $field.removeClass('error').attr('aria-invalid', 'false');
            }
        });
    });
})(jQuery);
