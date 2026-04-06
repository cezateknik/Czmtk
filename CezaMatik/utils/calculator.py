class PenaltyCalculator:
    def __init__(self):
        # Constants for time conversion
        self.DAYS_PER_MONTH = 30
        self.MONTHS_PER_YEAR = 12
        self.DAYS_PER_YEAR = 360  # 12 months * 30 days

    def convert_days_to_months_days(self, total_days):
        """Convert total days to months and days"""
        months = total_days // self.DAYS_PER_MONTH
        remaining_days = total_days % self.DAYS_PER_MONTH
        return months, remaining_days

    def calculate_penalty(self, years, months, days, fine, ratio, is_reduction):
        """
        Calculate the new penalty based on the provided inputs
        """

        # Ceza bileşenlerini gün cinsine çevir
        total_input_days = (years * self.DAYS_PER_YEAR) + (months * self.DAYS_PER_MONTH) + days

        year_days = years * self.DAYS_PER_YEAR
        month_day_days = (months * self.DAYS_PER_MONTH) + days

        if ratio == int(ratio) or isinstance(ratio, float):  # Tüm oranlar için kurala uygun hesap
            # Yıldan gelen günler → yıl’a çevrilebilir
            adjusted_year_days = year_days * ratio
            adjusted_years = int(adjusted_year_days // self.DAYS_PER_YEAR)
            remaining_days_from_years = adjusted_year_days % self.DAYS_PER_YEAR

            # Ay+gün kısmı → yıl’a çevrilmez, sadece gün → ay çevrilir
            adjusted_month_day_days = month_day_days * ratio
            total_months = int(adjusted_month_day_days // self.DAYS_PER_MONTH)
            remaining_days = adjusted_month_day_days % self.DAYS_PER_MONTH

            # Toplam artırım/indirim bileşenleri
            adjustment = {
                "years": adjusted_years,
                "months": total_months,
                "days": remaining_days_from_years + remaining_days
            }
        else:
            # Güvenli fallback (gerekirse)
            adjustment_days = total_input_days * ratio
            adjustment = self.days_to_years_months_days(adjustment_days)

        # Para cezası (fine) hesaplama
        if fine > 0:
            if is_reduction:
                fine_result = max(1, int(fine - (fine * ratio)))
            else:
                fine_result = int(fine + (fine * ratio))
        else:
            fine_result = 0

        if is_reduction:
            # Ceza azaltımı
            final_days = days - adjustment["days"]
            final_months = months - adjustment["months"]
            final_years = years - adjustment["years"]

            if final_days < 0:
                borrow_months = (-final_days + self.DAYS_PER_MONTH - 1) // self.DAYS_PER_MONTH
                final_months -= borrow_months
                final_days += borrow_months * self.DAYS_PER_MONTH

            if final_months < 0:
                borrow_years = (-final_months + self.MONTHS_PER_YEAR - 1) // self.MONTHS_PER_YEAR
                final_years -= borrow_years
                final_months += borrow_years * self.MONTHS_PER_YEAR

            final_years = max(0, final_years)
            final_months = max(0, final_months)
            final_days = max(0, final_days)
        else:
            # Ceza artırımı
            final_years = years + adjustment["years"]
            final_months = months + adjustment["months"]
            final_days = days + adjustment["days"]

            # Günler aya çevrilebilir
            extra_months, final_days = self.convert_days_to_months_days(final_days)
            final_months += extra_months

            # Aylar yıla çevrilmez! Ay 12'yi geçse bile sabit kalır

        # Ondalıklı gün varsa aşağı yuvarla
        final_days = int(final_days)

        return {
            "years": final_years,
            "months": final_months,
            "days": final_days,
            "fine": fine_result
        }

    def days_to_years_months_days(self, total_days):
        """
        Convert total days to years, months, and days
        """
        years = int(total_days) // self.DAYS_PER_YEAR
        remaining_days = int(total_days) % self.DAYS_PER_YEAR

        months = remaining_days // self.DAYS_PER_MONTH
        days = remaining_days % self.DAYS_PER_MONTH

        decimal_part = total_days - int(total_days)
        if decimal_part > 0:
            days += decimal_part

        return {
            "years": years,
            "months": months,
            "days": days
        }
