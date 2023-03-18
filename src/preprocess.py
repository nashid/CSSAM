import re


def word_tokenize(str):
    if str == '_':
        return list(str)
    str = str.strip().split('_')
    str_line = []
    for strs in str:
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', strs)
        str_line.extend([m.group(0) for m in matches])
    return str_line


def brief_code_process(str):
    str=re.sub('\n','',str)
    str=re.sub(' +',' ',str)
    return str


def str_process(str,dtype = 'code'):
    # str=re.sub('\t','<table>',str)
    str = re.sub('\n', r' ', str)
    str = re.sub(r'\t', r' ', str)
    str = re.sub(r'\\', ' ', str)
    str = re.sub('\(', ' ( ', str)
    str = re.sub('\)', ' ) ', str)
    str = re.sub('\,', ' , ', str)
    str = re.sub('\.', ' . ', str)
    str = re.sub('\.\s\s\.\s\s\.', '...', str)
    str = re.sub('\{', ' { ', str)
    str = re.sub('\}', ' } ', str)
    str = re.sub('\[', ' [ ', str)
    str = re.sub('\]', ' ] ', str)
    str = re.sub('\:', ' : ', str)
    str = re.sub('\;', ' ; ', str)
    str = re.sub('\<', ' < ', str)
    str = re.sub('\>', ' > ', str)
    str = re.sub('->', ' -> ', str)
    str = re.sub('\+', ' + ', str)
    str = re.sub('-', ' - ', str)
    str = re.sub('\*', ' * ', str)
    str = re.sub('/', ' / ', str)
    str = re.sub('=', ' = ', str)
    str = re.sub('=\s\s=', '==', str)
    str = re.sub('\'', ' \' ', str)
    str = re.sub('\"', ' \" ', str)
    str = re.sub('!', ' ! ', str)
    str = re.sub('%', ' % ', str)
    str = re.sub('&', ' & ', str)
    str = re.sub('\|', ' | ', str)
    str = re.sub('\?', ' ? ', str)
    str = re.sub('\^', ' ^ ', str)
    str = re.sub('~', ' ~ ', str)
    str = re.sub('@', ' @ ', str)
    str = re.sub('#',' # ',str)
    if dtype=='code':
        str = re.sub('_', ' _ ', str)
    str = re.sub(' +', ' ', str)
    return str  # .lower()


def code_tokenize(str,dtype='code'):
    code = str_process(str, dtype).strip().split(' ')
    tmp = []
    for idx, item in enumerate(code):
        tmp.extend(word_tokenize(item))
    for i in range(len(tmp)):
        tmp[i] = tmp[i]
    # for i,item in enumerate(code):
    #     code[i]=code[i].lower()
    return tmp



if __name__ == '__main__':
    a=str_process('@Override public int runCommand(boolean mergeErrorIntoOutput,String... commands) throws IOException, InterruptedException {\\n  return runCommand(mergeErrorIntoOutput,new ArrayList<String>(Arrays.asList(commands)));\n}\n','code')
    print(a)
    print(code_tokenize('@Override public int runCommand(boolean mergeErrorIntoOutput,String... commands) throws IOException, InterruptedException {\n a=="\\n" return runCommand(mergeErrorIntoOutput,new ArrayList<String>(Arrays.asList(commands)));\n}\n',dtype='code'))
    print(word_tokenize('@Override public int runCommand(boolean mergeErrorIntoOutput,String... commands) throws IOException, InterruptedException {\n  return runCommand(mergeErrorIntoOutput,new ArrayList<String>(Arrays.asList(commands)));\n}\n'))
    print(word_tokenize(a))
    #b=r'private int findPLV(int M_PriceList_ID){\n  Timestamp priceDate=null;\n  String dateStr=Env.getContext(Env.getCtx(),p_WindowNo,\"DateOrdered\");\n  if (dateStr != null && dateStr.length() > 0)   priceDate=Env.getContextAsDate(Env.getCtx(),p_WindowNo,\"DateOrdered\");\n else {\n    dateStr=Env.getContext(Env.getCtx(),p_WindowNo,\"DateInvoiced\");\n    if (dateStr != null && dateStr.length() > 0)     priceDate=Env.getContextAsDate(Env.getCtx(),p_WindowNo,\"DateInvoiced\");\n  }\n  if (priceDate == null)   priceDate=new Timestamp(System.currentTimeMillis());\n  log.config(\"M_PriceList_ID=\" + M_PriceList_ID + \" - \"+ priceDate);\n  int retValue=0;\n  String sql=\"SELECT plv.M_PriceList_Version_ID, plv.ValidFrom \" + \"FROM M_PriceList pl, M_PriceList_Version plv \" + \"WHERE pl.M_PriceList_ID=plv.M_PriceList_ID\"+ \" AND plv.IsActive='Y'\"+ \" AND pl.M_PriceList_ID=? \"+ \"ORDER BY plv.ValidFrom DESC\";\n  try {\n    PreparedStatement pstmt=DB.prepareStatement(sql,null);\n    pstmt.setInt(1,M_PriceList_ID);\n    ResultSet rs=pstmt.executeQuery();\n    while (rs.next() && retValue == 0) {\n      Timestamp plDate=rs.getTimestamp(2);\n      if (!priceDate.before(plDate))       retValue=rs.getInt(1);\n    }\n    rs.close();\n    pstmt.close();\n  }\n catch (  SQLException e) {\n    log.log(Level.SEVERE,sql,e);\n  }\n  Env.setContext(Env.getCtx(),p_WindowNo,\"M_PriceList_Version_ID\",retValue);\n  return retValue;\n}\n'
