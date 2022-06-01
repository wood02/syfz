from django.db import models

# Create your models here.
from common.django.basemodel import BaseModel


class EvidenceImage(BaseModel):
    image = models.ImageField("佐证图片", upload_to="images/%Y/%m/%d")
    remark = models.CharField("备注", max_length=255, null=True, blank=True)

    class Meta:
        db_table = "alarm_evidence_image"
        verbose_name = "佐证图片"
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Hacker(BaseModel):
    SEX = (
        (0, '未知'),
        (1, '男'),
        (2, '女')
    )
    # 身份信息
    name = models.CharField('姓名', max_length=50, null=True, blank=True)
    sex = models.PositiveSmallIntegerField("性别", default=0, choices=SEX)
    age = models.PositiveSmallIntegerField("年龄", null=True, blank=True)
    occupation = models.CharField("职业", max_length=50, null=True, blank=True)
    native_place = models.CharField("籍贯", max_length=255, null=True, blank=True)
    address = models.CharField("位置", max_length=255, null=True, blank=True)
    network_id = models.CharField("网络ID", max_length=100, null=True, blank=True)
    email = models.EmailField("邮件", null=True, blank=True)
    qq = models.CharField("邮件", max_length=50, null=True, blank=True)
    phone = models.CharField("手机号", max_length=50, null=True, blank=True)
    id_number = models.CharField("身份证号", max_length=50, null=True, blank=True)
    other_info = models.CharField("其他身份信息", max_length=255, null=True, blank=True)
    photo = models.ImageField("照片", upload_to="images/%Y/%m/%d", blank=True, null=True)
    photo_source = models.CharField("照片来源", max_length=50, null=True, blank=True)

    # 攻击设施
    fingerprint_info = models.JSONField("指纹信息", default=list, null=True, blank=True)
    attack_ip = models.JSONField("攻击IP", default=list, null=True, blank=True)
    attack_type = models.JSONField("攻击手法", default=list, null=True, blank=True)
    virus_sample = models.JSONField("关联病毒", default=list, null=True, blank=True)
    vulnerability = models.JSONField("关联漏洞", default=list, null=True, blank=True)
    domain = models.JSONField("关联域名", default=list, null=True, blank=True)
    other_facilities = models.JSONField("其他设施", default=list, null=True, blank=True)

    # 佐证截图
    evidence_image = models.ManyToManyField(EvidenceImage, related_name="hacker_evidence", verbose_name="佐证图片")

    # 服务器信息
    # sever_info = models.JSONField("其他设施", default=list, null=True, blank=True)

    class Meta:
        db_table = "alarm_hacker"
        verbose_name = "黑客"
        verbose_name_plural = verbose_name
        ordering = ['-id']


class EventFile(BaseModel):
    filename = models.CharField('附件名字', max_length=255, null=True, blank=True)
    event_file = models.FileField("附件地址", upload_to="files/%Y/%m/%d")

    class Meta:
        db_table = "alarm_event_file"
        verbose_name = "事件附件"
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Event(BaseModel):
    title = models.CharField('事件标题', max_length=100)
    hacker = models.ManyToManyField(Hacker)
    event_file = models.ManyToManyField(EventFile)

    class Meta:
        db_table = "alarm_event"
        verbose_name = "事件"
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Attack(BaseModel):
    """
    主要展示
    """
    STATUS = (
        (0, '待反制'),
        (1, '正在反制'),
        (2, '已完成'),
    )
    MALICIOUS = (
        (0, '未知'),
        (1, '恶意'),
        (2, '非恶意'),
    )
    source_ip = models.GenericIPAddressField("IP", protocol='both')
    trace_rate = models.FloatField("溯源成功率", default=0.30, null=True, blank=True)
    attack_earliest_time = models.DateTimeField("攻击最早时间", null=True, blank=True)

    domain_num = models.IntegerField("域名数量", default=0)
    asset_num = models.IntegerField("资产数量", default=0)
    vul_num = models.IntegerField("漏洞数量", default=0)

    location = models.JSONField("地理位置", null=True, blank=True)
    judgments = models.JSONField("IP属性", default=list, null=True, blank=True)
    malicious = models.SmallIntegerField("恶意", default=0, choices=MALICIOUS, db_index=True)
    is_tag_info = models.BooleanField("是否搜索过标签/信誉", default=False)
    is_ip_query = models.BooleanField("是否搜索过ip分析", default=False)
    is_ip2_domain = models.BooleanField("是否搜索过ip2域名", default=False)
    hacker = models.ForeignKey(Hacker, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    fz_task_id = models.CharField("反制任务id", max_length=50, null=True, blank=True)
    fz_start_time = models.DateTimeField("反制任务开始时间", null=True, blank=True)
    fz_end_time = models.DateTimeField("反制任务结束时间", null=True, blank=True)
    fz_status = models.PositiveSmallIntegerField("反制状态", default=0, null=True, blank=True, choices=STATUS)
    fz_result_raw = models.JSONField("反制结果", default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.id}.{self.source_ip}-[{self.fz_task_id}]-[{self.get_fz_status_display()}]"

    class Meta:
        db_table = "alarm_attack"
        verbose_name = "攻击日志"
        verbose_name_plural = verbose_name
        ordering = ['-id']


class AttackDetails(BaseModel):
    attack_time = models.DateTimeField("攻击时间")
    destination_ip = models.CharField("攻击目标目的IP", max_length=255)
    attack_type = models.CharField("攻击类型", max_length=100, null=True, blank=True)
    source = models.CharField("来源", max_length=20, null=True, blank=True)
    attack = models.ForeignKey(
        'Attack',
        verbose_name='攻击日志',
        related_name='attack_details',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "alarm_attack_details"
        verbose_name = "攻击日志详情"
        verbose_name_plural = verbose_name
        ordering = ['-id']


class AttackWhite(BaseModel):
    white_ip = models.CharField("白名单IP", max_length=100)
    remark = models.CharField("备注", max_length=255, null=True, blank=True)

    class Meta:
        db_table = "alarm_white"
        verbose_name = "攻击白名单"
        verbose_name_plural = verbose_name
        ordering = ['-id']
