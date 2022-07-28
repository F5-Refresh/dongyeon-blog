## 프로젝트소개
간단한 블로그를 운용 할 수 있는 프로그램입니다.


## Path
|Url|Method|Description|
|---|----------|---|
sign_up|Post|회원가입
sign_in|Post|로그인
post|Get|게시물리스트 조회
post|Post|게시물 작성
post/<int:id>|Patch|게시물 수정
post/<int:id>|Delete|게시물 삭제(soft)
post/detail/<int:id>|Get|게시물 상세
post/like/<int:id>|Post|좋아요
post/search|Get|검색 및 필터링
post/comment/<int:id>|Post|댓글작성

## DB
![image](https://user-images.githubusercontent.com/91131029/181394291-8d358457-d1d5-4466-911c-a2f1400417eb.png)

    
