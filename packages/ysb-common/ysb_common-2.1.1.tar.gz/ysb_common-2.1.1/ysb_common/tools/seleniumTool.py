from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


class SeleniumTool():

    @staticmethod
    def click_js_tag(browser, tag, attribute, content):
        '''
        js处理弹窗提示-点击按钮(标签/属性/text)-模拟菜单点击
        :param browser:
        :param tag: 标签
        :param attribute: 属性
        :param content: text内容
        :return:
        '''
        script = """
            var tags = document.getElementsByTagName('""" + tag + """') ;   
            for(var i = 0 ; i < tags.length ; i ++) {
                var ageText = tags[i].innerHTML.trim() ;   
                if(tags[i].hasAttribute('""" + attribute + """') && ageText.indexOf('""" + content + """') != -1) {
                    tags[i].click() ;
                    break ;
                }
            }
            """
        browser.execute_script(script)

    @staticmethod
    def click_radio(browser, path):
        '''
        单选框(radio)选中
        :param browser:
        :param path:
        :return:
        '''
        elements = browser.find_elements_by_xpath(path)
        if elements:
            for element in elements:
                if (not element.is_selected()):
                    element.send_keys(Keys.SPACE)

    @staticmethod
    def selector_calendar(browser, id, date):
        '''
        js日历选择器('yyyy-MM-dd')
        :param browser:
        :param id:
        :param date: 'yyyy-MM-dd'
        :return:
        '''
        script = """
                        function setValue(){
                            document.getElementById('""" + id + """').removeAttribute("readonly");
                            document.getElementById('""" + id + """').value='""" + date + """';
                        }
                        setValue();
            """
        browser.execute_script(script)

    @staticmethod
    def select_css(driver, xpth, value):
        '''
        通用下拉框处理
        :param browser:
        :param xpth:
        :return:
        '''
        select = Select(driver.find_element_by_css_selector(xpth))
        select.select_by_visible_text(value)

    @staticmethod
    def menu_js(browser, xpath, key):
        '''
        js菜单模拟点击
        :param browser:
        :param xpath:
        :param key:
        :return:
        '''
        menu = browser.find_elements_by_xpath(xpath)
        if len(menu) > 0:
            for i in range(len(menu)):
                if key in menu[i].text:
                    browser.execute_script('arguments[0].click();', menu[i])
                    break

    # 新报表一般纳税人铺数
    @staticmethod
    def ybnsr_set_value_by_js(browser, id, value):
        """
        :param browser:
        :param id:
        :param value:
        :return:
        """
        script = """
                   function setandgetvalue(){
                           var input_ele =$('""" + id + """');
                           var input_attr =input_ele.attr("disabled");
                           console.log('值是：' + input_attr );
                           if(input_attr == undefined){
                                $(input_ele).val('');
                                $(input_ele).val('""" + value + """').blur().change();
                            }
                   }
                   value_input = setandgetvalue();
           """
        browser.execute_script(script)

    @staticmethod
    def clickbtn_no(browser, btn_type=settings.NO):
        """
        点击申报页面的弹框的取消按钮
        :param browser:
        :param btn_type:
        :return:
        """
        script = """
                var retData = {confirmMsg:"",errorMsg:""};
                var length =0;
                var $content =  $(".mini-messagebox-content-text");
                $content.each(function(){
                    var msg = $(this).text();
                    var $box = $(this).parentsUntil(".mini-messagebox").parent()
                    console.log($box[0])
                    var $btns = $box.find(".mini-button");
                    var $okBtn,$cancelBtn;
                    $btns.each(function(){
                        var $btn = $(this);
                        var $span = $(this).find(".mini-button-text");
                        if($span.text() == "确定" || $span.text() == "是"){
                            $okBtn = $btn;

                        }else if($span.text() == "取消" || $span.text() == "否"){
                            $cancelBtn = $btn;
                        }
                    });
                    if($okBtn != null && $cancelBtn != null){
                        retData.confirmMsg = retData.confirmMsg+ (msg +"；");
                        if('""" + btn_type + """' == '""" + settings.NO + """'){
                            $cancelBtn.click();
                        }else{
                            $okBtn.click();
                        }
                    }else if($okBtn != null){
                        retData.confirmMsg = retData.confirmMsg+ (msg +"；");
                        if('""" + btn_type + """' == '""" + settings.NO + """'){
                            $cancelBtn.click();
                        }else{
                            $okBtn.click();
                        }
                    } else if($cancelBtn == null){
                         retData.errorMsg = retData.errorMsg + (msg +"；");
                         $okBtn.click();
                    }
                });
                console.log(retData)
                return retData;
            """
        ret_data = browser.execute_script(script)
        print(ret_data)
        return ret_data

    @staticmethod
    def clickbtn(browser, btn_type=settings.OK):
        """
        点击申报页面弹框的确定按钮
        :param browser:
        :param btn_type:
        :return:
        """
        ret_data = {}
        script = """
                var retData = {confirmMsg:"",errorMsg:""};
                var length =0;
                var $content =  $(".mini-messagebox-content-text");
                $content.each(function(){
                    var msg = $(this).text();
                    var $box = $(this).parentsUntil(".mini-messagebox").parent()
                    //console.log($box[0])
                    var $btns = $box.find(".mini-button");
                    var $okBtn,$cancelBtn;
                    $btns.each(function(){
                        var $btn = $(this);
                        var $span = $(this).find(".mini-button-text");
                        if($span.text() == "确定" || $span.text() == "是"){
                            $okBtn = $btn;
                        }else if($span.text() == "取消" || $span.text() == "否"){
                            $cancelBtn = $btn;
                        }
                    });
                    if($okBtn != null && $cancelBtn != null){
                        retData.confirmMsg = retData.confirmMsg+ (msg +"；");
                        if('""" + btn_type + """' == '""" + settings.NO + """'){
                            $cancelBtn.click();
                        }else{
                            $okBtn.click();
                        }
                    }else if($okBtn != null){
                        retData.confirmMsg = retData.confirmMsg+ (msg +"；");
                        if('""" + btn_type + """' == '""" + settings.NO + """'){
                            $cancelBtn.click();
                        }else{
                            $okBtn.click();
                        }
                    } else if($cancelBtn == null && $okBtn != null){
                         retData.errorMsg = retData.errorMsg + (msg +"；");
                         $okBtn.click();
                    }
                });
                //console.log(retData)
                return retData;
            """
        # 判断页面是否有该元素
        elments = sbUtil.get_elments(self, browser, '.mini-messagebox-content-text')
        if elments:
            time.sleep(1)
            ret_data = browser.execute_script(script)
            time.sleep(1)
            success_url = browser.current_url
            while ret_data["confirmMsg"] != '':
                time.sleep(0.2)
                if '请确认您本期是否在主管税务机关或外出经营代开专用发票、鉴证咨询业代自开专用发票和住宿业代自开专用发票' in retData['confirmMsg']:
                    recontent = """return $(".mini-messagebox-content-text").text()"""
                    msg = browser.execute_script(recontent)
                    if '是否发生销售不动产' in msg:
                        ret_data= self.clickBtnNo(browser, settings.NO)
                        self.clickBtn(browser, settings.OK)
                time.sleep(1)
                elments = sbUtil.get_elments(self, browser, '.mini-messagebox-content-text')
                if elments:
                    # 引导式公告
                    yds_gg = """return $(".mini-messagebox-content-text").text()"""
                    msg = browser.execute_script(yds_gg)
                    if '根据财政部、税务总局2020年第13号、24号公告，' in msg:
                        browser.execute_script("document.querySelector('#closeZcTip').click()")
                        print(msg)
                        return msg
                    if '本期销售额已超免税标准，请继续申报' in msg:
                        browser.execute_script("$('.mini-button').click()")
                        print(msg)
                        return msg
                    if '是否发生销售不动产' in msg:
                        self.clickBtnNo(browser, settings.NO)
                        self.clickBtn(browser, settings.OK)
                    if '附加税单独申报原因' in msg:
                        print(msg)
                        return msg
                    time.sleep(1)
                    ret_data = browser.execute_script(script)
                    time.sleep(2)
                    success_url = browser.current_url
                    print(ret_data)
                else:
                    break
            if '/public/sb_success.html' in success_url:
                ret_data["errorMsg"] = ''
                ret_data['url'] = success_url
                return ret_data
            return ret_data
        else:
            ret_data["errorMsg"] = ""
            ret_data["confirmMsg"] = ""
            return ret_data

    # 判断js元素是否存在
    @staticmethod
    def get_node_by_js(browser, js_name):
        """
        判断js元素是否存在
        :param browser:
        :param js_name:
        :return:
        """
        flag = True
        try:
            browser.execute_script(js_name)
            return flag
        except:
            flag = False
            return flag

    # 显示等待通过css
    @staticmethod
    def get_elments(browser, elment):
        """
        显示等待通过css
        :param browser:
        :param elment:
        :return:
        """
        flag = True
        try:
            WebDriverWait(browser, 5, 0.5).until(
                EC.visibility_of_any_elements_located((By.CSS_SELECTOR, elment)))
            return flag
        except Exception as e:
            flag = False
            return flag

    # 显示等待by id
    @staticmethod
    def get_elments_by_id(browser, elment):
        """
        显示等待by id
        :param browser:
        :param elment:
        :return:
        """
        flag = True
        try:
            WebDriverWait(browser, 4, 0.5).until(
                            EC.visibility_of(browser.find_element(By.ID, elment)))
            return flag
        except Exception as e:
            flag = False
            return flag

    # 判断增值税主表、附列资料、明细表tab是否存在，存在就点击相应的tab的公共方法
    @staticmethod
    def click_tab_common(browser, tab_name):
        """
        判断报表是否存在
        :param browser:
        :param tab_name:
        :return:
        """
        tab_script = """
                           function click_tab(){
                               is_cur = '0';
                               tab_list = document.getElementsByClassName("mini-tab-text");
                               for(var i =0;i<tab_list.length;i++){
                                   if((tab_list[i].innerText).indexOf('""" + tab_name + """') > -1){
                                       is_cur = '1';
                                       tab_list[i].click();
                                       break;
                                   }
                               }
                               return is_cur;
                           }
                           is_cur = click_tab();
                           return is_cur;
           """
        is_cur = str(browser.execute_script(tab_script))
        return is_cur
