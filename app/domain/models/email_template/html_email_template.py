from string import Template


def get_html_text(adopter_name: str, animal_name: str, form_link: str) -> str:
    html_text = Template(
        """
            <!DOCTYPE html>
            <html dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="pt" style="padding:0;Margin:0">
            <head>
            <meta charset="UTF-8">
            <meta content="width=device-width, initial-scale=1" name="viewport">
            <meta name="x-apple-disable-message-reformatting">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta content="telephone=no" name="format-detection">
            <title>Template email</title><!--[if (mso 16)]>
                <style type="text/css">
                a {text-decoration: none;}
                </style>
                <![endif]--><!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--><!--[if gte mso 9]>
            <xml>
                <o:OfficeDocumentSettings>
                <o:AllowPNG></o:AllowPNG>
                <o:PixelsPerInch>96</o:PixelsPerInch>
                </o:OfficeDocumentSettings>
            </xml>
            <![endif]-->
            <style type="text/css">
            #outlook a {
                padding:0;
            }
            .ExternalClass {
                width:100%;
            }
            .ExternalClass,
            .ExternalClass p,
            .ExternalClass span,
            .ExternalClass font,
            .ExternalClass td,
            .ExternalClass div {
                line-height:100%;
            }
            .es-button {
                mso-style-priority:100!important;
                text-decoration:none!important;
            }
            a[x-apple-data-detectors] {
                color:inherit!important;
                text-decoration:none!important;
                font-size:inherit!important;
                font-family:inherit!important;
                font-weight:inherit!important;
                line-height:inherit!important;
            }
            .es-desk-hidden {
                display:none;
                float:left;
                overflow:hidden;
                width:0;
                max-height:0;
                line-height:0;
                mso-hide:all;
            }
            @media only screen and (max-width:600px) {h1 { font-size:30px!important; text-align:center } h2 { font-size:24px!important; text-align:center } h3 { font-size:18px!important; text-align:center } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:30px!important } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:24px!important } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:18px!important } .es-menu td a { font-size:14px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:14px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:14px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:12px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:inline-block!important } a.es-button, button.es-button { font-size:14px!important; display:inline-block!important } .es-btn-fw { border-width:10px 0px!important; text-align:center!important } .es-adaptive table, .es-btn-fw, .es-btn-fw-brdr, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0px!important } .es-m-p0r { padding-right:0px!important } .es-m-p0l { padding-left:0px!important } .es-m-p0t { padding-top:0px!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } .es-menu td { width:1%!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } .es-desk-hidden { display:table-row!important; width:auto!important; overflow:visible!important; max-height:inherit!important } }
            @media screen and (max-width:384px) {.mail-message-content { width:414px!important } }
            </style>
            </head>
            <body style="width:100%;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
            <div dir="ltr" class="es-wrapper-color" lang="pt" style="background-color:#FFFFFF"><!--[if gte mso 9]>
                        <v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
                            <v:fill type="tile" color="#ffffff"></v:fill>
                        </v:background>
                    <![endif]-->
            <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top;background-color:#FFFFFF">
                <tr style="border-collapse:collapse">
                <td valign="top" style="padding:0;Margin:0">
                <table class="es-header" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
                    <tr style="border-collapse:collapse">
                    <td align="center" style="padding:0;Margin:0">
                    <table class="es-header-body" cellspacing="0" cellpadding="0" bgcolor="#FFFFFF" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
                        <tr style="border-collapse:collapse">
                        <td align="left" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:20px;padding-right:20px">
                        <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                            <tr style="border-collapse:collapse">
                            <td valign="top" align="center" style="padding:0;Margin:0;width:560px">
                            <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                <tr style="border-collapse:collapse">
                                <td align="center" style="padding:0;Margin:0;font-size:0px"><a target="_blank" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#1376C8;font-size:14px"><img src="https://fcjnyrx.stripocdn.email/content/guids/CABINET_f32a864bf0ad1576388fa348576e02f654d8e7d14d04fa5fdd6a42e955afd7f6/images/logo.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="128"></a></td>
                                </tr>
                                <tr style="border-collapse:collapse">
                                <td align="center" style="padding:10px;Margin:0"><h1 style="Margin:0;line-height:48px;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;font-size:24px;font-style:normal;font-weight:bold;color:#000000">Olá $adopter_name,</h1></td>
                                </tr>
                            </table></td>
                            </tr>
                        </table></td>
                        </tr>
                    </table></td>
                    </tr>
                </table>
                <table class="es-content" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
                    <tr style="border-collapse:collapse">
                    <td style="padding:0;Margin:0;background-image:url(https://fcjnyrx.stripocdn.email/content/guids/CABINET_a906e668866a7123ea4f0e3eed846f3d/images/62941543406934823.png);background-position:center top;background-repeat:no-repeat" align="center" background="https://fcjnyrx.stripocdn.email/content/guids/CABINET_a906e668866a7123ea4f0e3eed846f3d/images/62941543406934823.png">
                    <table class="es-content-body" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px" cellspacing="0" cellpadding="0" bgcolor="transparent" align="center">
                        <tr style="border-collapse:collapse">
                        <td style="Margin:0;padding-bottom:20px;padding-left:20px;padding-right:20px;padding-top:30px;background-color:transparent" bgcolor="transparent" align="left"><!--[if mso]><table style="width:560px" cellpadding="0" 
                                    cellspacing="0"><tr><td style="width:270px" valign="top"><![endif]-->
                        <table class="es-left" cellspacing="0" cellpadding="0" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                            <tr style="border-collapse:collapse">
                            <td class="es-m-p20b" align="left" style="padding:0;Margin:0;width:270px">
                            <table style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-position:center center" width="100%" cellspacing="0" cellpadding="0">
                                <tr style="border-collapse:collapse">
                                <td align="center" style="padding:0;Margin:0;font-size:0"><img class="adapt-img" src="https://fcjnyrx.stripocdn.email/content/guids/CABINET_504165bc0ba6cef605507669c4ebeb6d/images/94371543403004731.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;width:270px;height:241.867px" width="270"></td>
                                </tr>
                            </table></td>
                            </tr>
                        </table><!--[if mso]></td><td style="width:20px"></td><td style="width:270px" valign="top"><![endif]-->
                        <table class="es-right" cellspacing="0" cellpadding="0" align="right" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                            <tr style="border-collapse:collapse">
                            <td align="left" style="padding:0;Margin:0;width:270px">
                            <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                <tr style="border-collapse:collapse">
                                <td align="left" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;line-height:27px;color:#333333;font-size:18px"><strong>Obrigado por considerar a adoção de $animal_name! Por favor, preencha nosso formulário clicando no link abaixo.</strong></p></td>
                                </tr>
                                <tr style="border-collapse:collapse">
                                <td align="center" style="padding:0;Margin:0"><span class="es-button-border" style="border-style:solid;border-color:transparent;background:#06f638;border-width:0px;display:inline-block;border-radius:8px;width:auto"><a href="$form_link" class="es-button" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#000000;font-size:14px;display:inline-block;background:#06f638;border-radius:8px;font-family:arial, 'helvetica neue', helvetica, sans-serif;font-weight:bold;font-style:normal;line-height:17px;width:auto;text-align:center;padding:10px 20px 10px 20px;mso-padding-alt:0;mso-border-alt:10px solid #06f638">Link</a></span></td>
                                </tr>
                            </table></td>
                            </tr>
                        </table><!--[if mso]></td></tr></table><![endif]--></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
            </table>
            </div>
            </body>
            </html>
        """
    )

    return html_text.substitute(adopter_name=adopter_name, animal_name=animal_name, form_link=form_link)
