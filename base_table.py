
from sqlalchemy import create_engine, Column, String, Integer, BigInteger, DECIMAL, Enum,DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'  # 这里请替换为您的数据表名

    id = Column(Integer, primary_key=True, autoincrement=True)

    # 这里请根据您的数据表结构添加其他字段，例如：创建新的数据列可以用到查询随便填
    password = Column(String(100))

    tokens = Column(BigInteger)
    Email = Column(String(100), primary_key=True)
    Number = Column(Integer)
    Balance = Column(DECIMAL(precision=8, scale=3))
    google_id = Column(String(50))
    github_id = Column(String(50))
    # content = Column(String(500))
    def __str__(self):
        return f"User: {self.username}, Tokens: {self.tokens}, Balance: {self.Balance}"

class Email(Base):
    __tablename__ = 'email'  # 这里请替换为您的数据表名

    id = Column(Integer, primary_key=True)
    email = Column(String(100), primary_key=True)
    exist = Column(Boolean)

    # content = Column(String(500))
    def __str__(self):
        return f"id: {self.id},email: {self.email}, exist: {self.exist}"
class documents(Base):
    __tablename__ = 'documents'  # 这里请替换为您的数据表名


    # 这里请根据您的数据表结构添加其他字段，例如：创建新的数据列可以用到查询随便填
    title = Column(String(100))
    states = Column(Boolean)
    Usage = Column(DECIMAL(precision=5, scale=3))
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    url = Column(String(100))
    create_at = Column(DateTime)

    def __str__(self):
        return f"Document: {self.title}, State: {self.states}, Usage: {self.Usage}, Order ID: {self.order_id}, User ID: {self.user_id}, URL: {self.url}, Created At: {self.create_at}"

class trade_number(Base):
    __tablename__ = 'trade_number'  # 这里请替换为您的数据表名

    amount = Column(DECIMAL(precision=6, scale=2))
    statue = Column(Boolean)
    number = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer)

    create_at = Column(DateTime)


    # content = Column(String(500))
    # def __str__(self):
    #     return f"User: {self.username}, Tokens: {self.tokens}, Balance: {self.Balance}"

# SQLAlchemy URI格式：dialect+driver://username:password@host:port/database
# DATABASE_URI = 'mysql+pymysql://root:abc123@localhost:3306/paper'
#
# engine = create_engine(DATABASE_URI)
# Session = sessionmaker(bind=engine)

# def get_paper_by_id(paper_id):
#     session = Session()
#     user = session.query(User).filter_by(id=paper_id,password='1421243966god').first()
#     session.close()
#     return user
#
# # 调用函数进行查询
# paper = get_paper_by_id(2)
# print(paper)
# print(paper.github_id)
