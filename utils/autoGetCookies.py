from typing import Union, Any
from rookiepy import edge, chrome, firefox


class getCookies:
    def __init__(
            self,
            domainName: str = ".singlelogin.re",
            _browser: Union[Any, edge] = edge
        ) -> None:
        """
        通过浏览器获取cookies
        :param domainName: str = ".singlelogin.re" 需要获取的域名
        :param _browser: Union[Any, edge] = edge 选择需要获取的浏览器
        :return None
        """
        self.domain_name = domainName
        self.browser = _browser

    def get(self, key: Union[str, None] = None) -> Union[str, None]:
        """
        通过key从cookies中提取value
        :param key: Union[str, None] = None 默认None时返回所有值
        :return Union[str, None]
        """
        if not self.browser:
            return None
        
        result = ""
        cookies = self.browser()
        if not cookies:
            return None
        
        for cookie in cookies:
            if cookie['domain'] != self.domain_name:
                continue
            if key is not None and key == cookie['name']:
                result = cookie['value']
                break

            result += f"{cookie['name']}={cookie['value']}; "

        return result
        

if __name__ == "__main__":
    # test
    print(getCookies().get())
    print(getCookies().get("remix_userid"))
    print(getCookies().get("remix_userkey"))
    