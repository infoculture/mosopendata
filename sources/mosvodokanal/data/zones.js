                var rsv = {
                    name: 'Рублевская',
                    href: 'http://www.mosvodokanal.ru/index.php?do=cat&category=rublevo_ct'
                },
                ssv = {
                    name: 'Северная',
                    href: 'http://www.mosvodokanal.ru/index.php?do=cat&category=cever_ct'
                },
                vsv = {
                    name: 'Восточная',
                    href: 'http://www.mosvodokanal.ru/index.php?do=cat&category=voctok_ct'
                },
                zsv = {
                    name: 'Западная',
                    href: 'http://www.mosvodokanal.ru/index.php?do=cat&category=zapad_ct'
                },
                mis = {
                    name: 'Москворецкий',
                    href: 'http://www.mosvodokanal.ru/index.php?do=cat&category=mos_istoch'
                },
                vis = {
                    name: 'Волжский',
                    href: 'http://www.mosvodokanal.ru/index.php?do=cat&category=vol_istoch'
                };

                if (zones) {
                    var zn = [],
                        ist = [],
                        hrefs = [],
                        isArt = false;

                    $.each(zones, function(i, zone) {
                        switch (zone.id) {
                            case '1':
                                zn[zn.length] = rsv;
                                ist[ist.length] = mis;
                                break;
                            case '2':
                                zn[zn.length] = vsv;
                                ist[ist.length] = vis;
                                break;
                            case '3':
                                zn[zn.length] = ssv;
                                ist[ist.length] = vis;
                                break;
                            case '4':
                                zn[zn.length] = zsv;
                                ist[ist.length] = mis;
                                break;
                            case '9':
                                isArt = true;
                                break;
                        }
                    });